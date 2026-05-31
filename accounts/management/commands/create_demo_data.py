from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Profile
from equipment.models import Equipment


class Command(BaseCommand):
    help = "Create local demo users and sample equipment for presentation only."

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True})
        admin.set_password("Admin@12345")
        admin.save()
        Profile.objects.update_or_create(user=admin, defaults={"role": Profile.ROLE_ADMIN})

        user, created = User.objects.get_or_create(username="user1", defaults={"email": "user1@example.com"})
        user.set_password("User@12345")
        user.save()
        Profile.objects.update_or_create(user=user, defaults={"role": Profile.ROLE_USER})

        samples = [
            ("Oscilloscope", "Electronics", "Digital lab oscilloscope for signal testing.", 3, Equipment.STATUS_AVAILABLE),
            ("Arduino Kit", "Microcontroller", "Starter kit with board, cable, and sensors.", 10, Equipment.STATUS_AVAILABLE),
            ("Soldering Station", "Tools", "Temperature-controlled soldering station.", 0, Equipment.STATUS_NOT_AVAILABLE),
        ]
        for name, category, description, quantity, status in samples:
            Equipment.objects.update_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "quantity_available": quantity,
                    "status": status,
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo users and equipment created."))
