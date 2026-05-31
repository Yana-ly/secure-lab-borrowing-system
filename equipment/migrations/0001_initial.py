# Generated for Secure Lab Equipment Borrowing System.
from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Equipment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, validators=[django.core.validators.RegexValidator("^[A-Za-z0-9 .,_()-]+$", "Use safe characters only.")])),
                ("category", models.CharField(max_length=80)),
                ("description", models.TextField(blank=True)),
                ("quantity_available", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ("status", models.CharField(choices=[("AVAILABLE", "Available"), ("NOT_AVAILABLE", "Not Available")], default="AVAILABLE", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="BorrowRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("purpose", models.TextField()),
                ("borrow_date", models.DateField()),
                ("return_date", models.DateField()),
                ("status", models.CharField(choices=[("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")], default="PENDING", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("equipment", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="borrow_requests", to="equipment.equipment")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="borrow_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
