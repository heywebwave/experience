from django.core.management.base import BaseCommand
from core.models import Event

class Command(BaseCommand):
    help = 'Updates event status based on event date'

    def handle(self, *args, **kwargs):
        Event.update_all_event_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated event status')) 