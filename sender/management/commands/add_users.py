from django.core.management import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = "Create new users"

    def handle(self, *args, **options):
        CustomUser.objects.all().delete()
        CustomUser.objects.create_superuser(
            username="admin",
            email="admin@mail.ru",
            password="admin",
            is_active=True,
            is_staff=True,
        )
        CustomUser.objects.create_user(
            username="manager",
            email="manager@mail.ru",
            password="manager",
            is_active=True,
            is_staff=True,
        )
        CustomUser.objects.create_user(
            username="user", email="user@mail.ru", password="user", is_active=True
        )
