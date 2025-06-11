from django.core.management.base import BaseCommand
from django.core.management import call_command
from sender.models import Message


class Command(BaseCommand):
    help = 'Adds test recipients to database'

    def handle(self, *args, **options):
        Message.objects.all().delete()
        call_command('loaddata', 'messages_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully added messages'))