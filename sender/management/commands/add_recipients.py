from django.core.management.base import BaseCommand
from django.core.management import call_command
from sender.models import Recipient

class Command(BaseCommand):
    help = 'Adds test recipients to database'

    def handle(self, *args, **options):
        Recipient.objects.all().delete()
        call_command('loaddata', 'recipients_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully added recipients'))