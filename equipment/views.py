from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required, is_admin_user
from audit.models import AuditLog
from audit.utils import log_audit

from .forms import BorrowRequestForm, EquipmentForm
from .models import BorrowRequest, Equipment


@login_required
def dashboard(request):
    if is_admin_user(request.user):
        context = {
            "total_requests": BorrowRequest.objects.count(),
            "pending_requests": BorrowRequest.objects.filter(status=BorrowRequest.STATUS_PENDING).count(),
            "approved_requests": BorrowRequest.objects.filter(status=BorrowRequest.STATUS_APPROVED).count(),
            "failed_logins": AuditLog.objects.filter(action="LOGIN_FAILED").count(),
            "equipment_count": Equipment.objects.count(),
            "requests": BorrowRequest.objects.select_related("user", "equipment")[:5],
            "recent_logs": AuditLog.objects.select_related("user")[:6],
        }
    else:
        my_requests = BorrowRequest.objects.filter(user=request.user)
        context = {
            "available_equipment": Equipment.objects.filter(status=Equipment.STATUS_AVAILABLE, quantity_available__gt=0),
            "my_requests": my_requests.select_related("equipment")[:5],
            "total_requests": my_requests.count(),
            "pending_requests": my_requests.filter(status=BorrowRequest.STATUS_PENDING).count(),
            "approved_requests": my_requests.filter(status=BorrowRequest.STATUS_APPROVED).count(),
            "rejected_requests": my_requests.filter(status=BorrowRequest.STATUS_REJECTED).count(),
        }
    return render(request, "equipment/dashboard.html", context)


@login_required
def equipment_list(request):
    if is_admin_user(request.user):
        equipment = Equipment.objects.all()
    else:
        equipment = Equipment.objects.filter(status=Equipment.STATUS_AVAILABLE, quantity_available__gt=0)
    return render(request, "equipment/equipment_list.html", {"equipment": equipment})


@login_required
@admin_required
def equipment_create(request):
    form = EquipmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save()
        log_audit(request.user, "EQUIPMENT_CREATED", request, f"Equipment created: {item.name}")
        messages.success(request, "Equipment created.")
        return redirect("equipment:equipment_list")
    return render(request, "equipment/equipment_form.html", {"form": form, "title": "Create Equipment"})


@login_required
@admin_required
def equipment_update(request, pk):
    item = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        item = form.save()
        log_audit(request.user, "EQUIPMENT_UPDATED", request, f"Equipment updated: {item.name}")
        messages.success(request, "Equipment updated.")
        return redirect("equipment:equipment_list")
    return render(request, "equipment/equipment_form.html", {"form": form, "title": "Edit Equipment"})


@login_required
@admin_required
def equipment_delete(request, pk):
    item = get_object_or_404(Equipment, pk=pk)
    if request.method == "POST":
        name = item.name
        try:
            item.delete()
        except ProtectedError:
            messages.error(request, "Equipment cannot be deleted because borrowing requests still reference it.")
            return redirect("equipment:equipment_list")
        log_audit(request.user, "EQUIPMENT_DELETED", request, f"Equipment deleted: {name}")
        messages.success(request, "Equipment deleted.")
        return redirect("equipment:equipment_list")
    return render(request, "equipment/confirm_delete.html", {"object": item, "title": "Delete Equipment"})


@login_required
def request_list(request):
    if is_admin_user(request.user):
        requests = BorrowRequest.objects.select_related("user", "equipment")
        template = "equipment/admin_request_list.html"
    else:
        requests = BorrowRequest.objects.filter(user=request.user).select_related("equipment")
        template = "equipment/request_list.html"
    return render(request, template, {"requests": requests})


@login_required
def request_create(request):
    if is_admin_user(request.user):
        log_audit(request.user, "UNAUTHORIZED_ACCESS", request, "Admin attempted to use normal-user request creation page.")
        raise PermissionDenied
    form = BorrowRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        borrow_request = form.save(commit=False)
        borrow_request.user = request.user
        borrow_request.status = BorrowRequest.STATUS_PENDING
        # All persistence uses Django ORM. No raw SQL is used, which prevents SQL injection through parameterized queries.
        borrow_request.save()
        log_audit(request.user, "REQUEST_CREATED", request, f"Borrow request created for {borrow_request.equipment.name}.")
        messages.success(request, "Borrowing request submitted.")
        return redirect("equipment:request_list")
    return render(request, "equipment/request_form.html", {"form": form, "title": "Create Borrowing Request"})


def _get_owned_pending_request(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)
    if borrow_request.user != request.user:
        log_audit(request.user, "UNAUTHORIZED_ACCESS", request, f"IDOR attempt blocked for request {pk}.")
        raise PermissionDenied
    if borrow_request.status != BorrowRequest.STATUS_PENDING:
        messages.error(request, "Only pending requests can be changed.")
        raise PermissionDenied
    return borrow_request


@login_required
def request_update(request, pk):
    borrow_request = _get_owned_pending_request(request, pk)
    form = BorrowRequestForm(request.POST or None, instance=borrow_request)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_audit(request.user, "REQUEST_UPDATED", request, f"Borrow request {pk} updated.")
        messages.success(request, "Borrowing request updated.")
        return redirect("equipment:request_list")
    return render(request, "equipment/request_form.html", {"form": form, "title": "Edit Borrowing Request"})


@login_required
def request_delete(request, pk):
    borrow_request = _get_owned_pending_request(request, pk)
    if request.method == "POST":
        borrow_request.delete()
        log_audit(request.user, "REQUEST_DELETED", request, f"Borrow request {pk} deleted.")
        messages.success(request, "Borrowing request deleted.")
        return redirect("equipment:request_list")
    return render(request, "equipment/confirm_delete.html", {"object": borrow_request, "title": "Delete Borrowing Request"})


@login_required
@admin_required
def request_approve(request, pk):
    borrow_request = get_object_or_404(BorrowRequest.objects.select_related("equipment"), pk=pk)
    if request.method == "POST":
        if borrow_request.status != BorrowRequest.STATUS_PENDING:
            messages.error(request, "Only pending requests can be approved.")
            return redirect("equipment:request_list")
        with transaction.atomic():
            equipment = Equipment.objects.select_for_update().get(pk=borrow_request.equipment.pk)
            if equipment.status != Equipment.STATUS_AVAILABLE or borrow_request.quantity > equipment.quantity_available:
                messages.error(request, "Request cannot be approved because equipment is no longer available in that quantity.")
                return redirect("equipment:request_list")
            equipment.quantity_available -= borrow_request.quantity
            if equipment.quantity_available == 0:
                equipment.status = Equipment.STATUS_NOT_AVAILABLE
            equipment.save(update_fields=["quantity_available", "status", "updated_at"])
            borrow_request.status = BorrowRequest.STATUS_APPROVED
            borrow_request.save(update_fields=["status", "updated_at"])
            log_audit(request.user, "REQUEST_APPROVED", request, f"Borrow request {pk} approved.")
            messages.success(request, "Request approved.")
    return redirect("equipment:request_list")


@login_required
@admin_required
def request_reject(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)
    if request.method == "POST":
        if borrow_request.status != BorrowRequest.STATUS_PENDING:
            messages.error(request, "Only pending requests can be rejected.")
            return redirect("equipment:request_list")
        borrow_request.status = BorrowRequest.STATUS_REJECTED
        borrow_request.save(update_fields=["status", "updated_at"])
        log_audit(request.user, "REQUEST_REJECTED", request, f"Borrow request {pk} rejected.")
        messages.success(request, "Request rejected.")
    return redirect("equipment:request_list")


@login_required
@admin_required
def admin_request_delete(request, pk):
    borrow_request = get_object_or_404(BorrowRequest, pk=pk)
    if request.method == "POST":
        borrow_request.delete()
        log_audit(request.user, "REQUEST_DELETED_BY_ADMIN", request, f"Admin deleted borrow request {pk}.")
        messages.success(request, "Request deleted.")
        return redirect("equipment:request_list")
    return render(request, "equipment/confirm_delete.html", {"object": borrow_request, "title": "Delete Borrowing Request"})
