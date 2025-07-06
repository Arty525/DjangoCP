from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = "Create new groups"

    def handle(self, *args, **options):
        Group.objects.all().delete()
        # Создаем новую группу для менеджеров
        manager = Group.objects.create(name="Manager")

        # Получаем разрешения на добавление и изменение данных
        view_mailing_list_permission = Permission.objects.get(
            codename="can_view_mailing_list"
        )
        view_recipient_permission = Permission.objects.get(
            codename="can_view_recipient"
        )
        view_user_list_permission = Permission.objects.get(
            codename="can_view_user_list"
        )
        view_message_permission = Permission.objects.get(codename="can_view_message")
        view_attempts_permission = Permission.objects.get(codename="can_view_attempts")
        ban_permission = Permission.objects.get(codename="can_ban")
        turn_off_permission = Permission.objects.get(codename="can_turn_off")

        # Назначаем разрешения группе
        manager.permissions.add(
            view_mailing_list_permission,
            view_recipient_permission,
            view_user_list_permission,
            view_message_permission,
            view_attempts_permission,
            ban_permission,
            turn_off_permission,
        )
        manager.save()

        # Создаем новую группу для админа
        admin_group = Group.objects.create(name="Administrator")
        admin_group.save()

        # Добавляем пользователей в группы
        admin = CustomUser.objects.get(username="admin")
        admin.groups.add(admin_group)

        pm = CustomUser.objects.get(username="manager")
        pm.groups.add(manager)
