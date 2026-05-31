from .models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_audit(user, action, request, description=""):
    """Central audit helper. Never pass passwords, tokens, or secrets in description."""
    AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        ip_address=get_client_ip(request),
        description=description[:500],
    )
