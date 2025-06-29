from django.core.management.base import BaseCommand
from story.models import Story
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete expired stories from the database'

    def handle(self, *args, **kwargs):
        expired = Story.objects.filter(expires_at__lt=timezone.now())
        count = expired.count()
        expired.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} expired stories'))
