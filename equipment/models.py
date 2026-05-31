from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Equipment(models.Model):
    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_NOT_AVAILABLE = "NOT_AVAILABLE"
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_NOT_AVAILABLE, "Not Available"),
    ]

    name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r"^[A-Za-z0-9 .,_()-]+$", "Use safe characters only.")],
    )
    category = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    quantity_available = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BorrowRequest(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrow_requests")
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name="borrow_requests")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    purpose = models.TextField()
    borrow_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.status})"
