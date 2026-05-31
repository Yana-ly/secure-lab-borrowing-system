from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.decorators import admin_required

from .models import AuditLog


@login_required
@admin_required
def audit_log_list(request):
    logs = AuditLog.objects.select_related("user")[:200]
    return render(request, "audit/audit_log_list.html", {"logs": logs})
