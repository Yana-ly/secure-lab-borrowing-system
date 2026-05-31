from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from audit.models import AuditLog


class AuthenticationAuditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="student1",
            email="student1@example.com",
            password="Student@12345",
        )
        Profile.objects.create(user=self.user, role=Profile.ROLE_USER)

    def test_failed_login_is_audited_without_password(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "student1", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        log = AuditLog.objects.get(action="LOGIN_FAILED")
        self.assertIn("student1", log.description)
        self.assertNotIn("wrong-password", log.description)

    def test_successful_logout_is_audited(self):
        login_ok = self.client.login(username="student1", password="Student@12345")
        self.assertTrue(login_ok)

        self.client.post(reverse("accounts:logout"))

        self.assertTrue(AuditLog.objects.filter(action="LOGOUT", user=self.user).exists())


class RegistrationValidationTests(TestCase):
    def test_registration_rejects_weak_password(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "password1": "password",
                "password2": "password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_registration_creates_normal_user_profile(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "password1": "BlueRiver@12345",
                "password2": "BlueRiver@12345",
            },
        )

        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="newstudent")
        self.assertEqual(user.profile.role, Profile.ROLE_USER)
