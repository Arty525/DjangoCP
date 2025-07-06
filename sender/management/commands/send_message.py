from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from sender.models import MailingList
from users.models import CustomUser


class Command(BaseCommand):
    help = "Create new users"

    def handle(self, *args, **options):
        username = input("Введите ваш email: ")
        user = get_object_or_404(CustomUser, email=username)
        mailing_lists = MailingList.objects.filter(owner=user)
        print("Список доступных рассылок:")
        for mailing_list in mailing_lists.filter(is_active=True):
            print(mailing_list)

        pk = input("Введите id рассылки: ")

        mailing_list = get_object_or_404(MailingList, id=pk)
        if mailing_list:
            mailing_list.send()
        else:
            print("Не удалось выполнить рассылку")
