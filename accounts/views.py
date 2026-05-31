from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render

from audit.utils import log_audit
from equipment.models import BorrowRequest

from .forms import ProfileAttachmentForm, RegistrationForm, SecureAuthenticationForm
from .models import Profile


class SecureLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = SecureAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(self.request.user, "LOGIN_SUCCESS", self.request, "Successful login.")
        return response

    def form_invalid(self, form):
        username = self.request.POST.get("username", "unknown")
        log_audit(None, "LOGIN_FAILED", self.request, f"Failed login for username: {username}")
        return super().form_invalid(form)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Profile.objects.create(user=user, role=Profile.ROLE_USER)
            log_audit(user, "USER_REGISTERED", request, "New normal user registered.")
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("accounts:login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
@require_POST
def logout_view(request):
    log_audit(request.user, "LOGOUT", request, "User logged out.")
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileAttachmentForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile attachment updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileAttachmentForm(instance=profile_obj)

    requests = BorrowRequest.objects.filter(user=request.user)
    context = {
        "profile_obj": profile_obj,
        "form": form,
        "total_requests": requests.count(),
        "approved_requests": requests.filter(status=BorrowRequest.STATUS_APPROVED).count(),
        "pending_requests": requests.filter(status=BorrowRequest.STATUS_PENDING).count(),
        "rejected_requests": requests.filter(status=BorrowRequest.STATUS_REJECTED).count(),
    }
    return render(request, "accounts/profile.html", context)


def permission_denied_view(request, exception=None):
    return render(request, "403.html", status=403)


def not_found_view(request, exception=None):
    return render(request, "404.html", status=404)


def server_error_view(request):
    return render(request, "500.html", status=500)
