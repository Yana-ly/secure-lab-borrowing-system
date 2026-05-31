from functools import wraps

from django.core.exceptions import PermissionDenied

from audit.utils import log_audit


def is_admin_user(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "ADMIN"


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_admin_user(request.user):
            log_audit(request.user if request.user.is_authenticated else None, "UNAUTHORIZED_ACCESS", request, "Admin-only page blocked.")
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped
