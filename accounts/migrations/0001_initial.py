# Generated for Secure Lab Equipment Borrowing System.
from django.conf import settings
from django.db import migrations, models
import accounts.models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("ADMIN", "Admin"), ("USER", "Normal User")], default="USER", max_length=10)),
                ("attachment", models.FileField(blank=True, help_text="Optional PDF/JPG/PNG proof document, max 2MB.", null=True, upload_to=accounts.models.profile_upload_path, validators=[accounts.models.validate_profile_file])),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
