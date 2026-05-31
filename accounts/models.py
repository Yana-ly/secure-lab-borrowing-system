import os
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def profile_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"profile_attachments/{uuid.uuid4()}{ext}"


def validate_profile_file(file):
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png"}
    allowed_content_types = {"application/pdf", "image/jpeg", "image/png"}
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError("Only PDF, JPG, and PNG files are allowed.")
    if getattr(file, "content_type", None) not in allowed_content_types:
        raise ValidationError("Invalid file type.")
    if file.size > 2 * 1024 * 1024:
        raise ValidationError("File size must not exceed 2MB.")


class Profile(models.Model):
    ROLE_ADMIN = "ADMIN"
    ROLE_USER = "USER"
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER, "Normal User"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    attachment = models.FileField(
        upload_to=profile_upload_path,
        validators=[validate_profile_file],
        blank=True,
        null=True,
        help_text="Optional PDF/JPG/PNG proof document, max 2MB.",
    )

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
