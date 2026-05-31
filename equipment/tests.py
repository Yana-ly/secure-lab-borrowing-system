from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Profile
from audit.models import AuditLog
from equipment.forms import BorrowRequestForm
from equipment.models import BorrowRequest, Equipment


class BorrowRequestValidationTests(TestCase):
    def setUp(self):
        self.equipment = Equipment.objects.create(
            name="Signal Generator",
            category="Electronics",
            description="Function generator",
            quantity_available=2,
            status=Equipment.STATUS_AVAILABLE,
        )

    def test_rejects_past_borrow_date_and_excess_quantity(self):
        form = BorrowRequestForm(
            data={
                "equipment": self.equipment.pk,
                "quantity": 5,
                "purpose": "Testing",
                "borrow_date": timezone.localdate() - timedelta(days=1),
                "return_date": timezone.localdate() + timedelta(days=1),
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("borrow_date", form.errors)
        self.assertIn("quantity", form.errors)

    def test_rejects_not_available_equipment(self):
        self.equipment.status = Equipment.STATUS_NOT_AVAILABLE
        self.equipment.save()

        form = BorrowRequestForm(
            data={
                "equipment": self.equipment.pk,
                "quantity": 1,
                "purpose": "Testing",
                "borrow_date": timezone.localdate() + timedelta(days=1),
                "return_date": timezone.localdate() + timedelta(days=2),
            }
        )

        self.assertFalse(form.is_valid())


class RoleAccessControlTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin2", "admin2@example.com", "Admin@12345")
        Profile.objects.create(user=self.admin, role=Profile.ROLE_ADMIN)
        self.owner = User.objects.create_user("owner", "owner@example.com", "Owner@12345")
        Profile.objects.create(user=self.owner, role=Profile.ROLE_USER)
        self.other = User.objects.create_user("other", "other@example.com", "Other@12345")
        Profile.objects.create(user=self.other, role=Profile.ROLE_USER)
        self.equipment = Equipment.objects.create(
            name="Oscilloscope",
            category="Electronics",
            description="Digital oscilloscope",
            quantity_available=2,
            status=Equipment.STATUS_AVAILABLE,
        )
        self.borrow_request = BorrowRequest.objects.create(
            user=self.owner,
            equipment=self.equipment,
            quantity=1,
            purpose="Lab assignment",
            borrow_date=timezone.localdate() + timedelta(days=1),
            return_date=timezone.localdate() + timedelta(days=2),
        )

    def test_normal_user_cannot_access_admin_pages(self):
        self.client.login(username="owner", password="Owner@12345")

        response = self.client.get(reverse("audit:audit_log_list"))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(AuditLog.objects.filter(action="UNAUTHORIZED_ACCESS", user=self.owner).exists())

    def test_idor_edit_and_delete_are_blocked(self):
        self.client.login(username="other", password="Other@12345")

        edit_response = self.client.get(reverse("equipment:request_update", args=[self.borrow_request.pk]))
        delete_response = self.client.get(reverse("equipment:request_delete", args=[self.borrow_request.pk]))

        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_admin_approval_reduces_available_quantity_once(self):
        self.client.login(username="admin2", password="Admin@12345")

        first = self.client.post(reverse("equipment:request_approve", args=[self.borrow_request.pk]))
        self.equipment.refresh_from_db()
        self.borrow_request.refresh_from_db()

        self.assertRedirects(first, reverse("equipment:request_list"))
        self.assertEqual(self.borrow_request.status, BorrowRequest.STATUS_APPROVED)
        self.assertEqual(self.equipment.quantity_available, 1)

        second = self.client.post(reverse("equipment:request_approve", args=[self.borrow_request.pk]))
        self.equipment.refresh_from_db()

        self.assertRedirects(second, reverse("equipment:request_list"))
        self.assertEqual(self.equipment.quantity_available, 1)
