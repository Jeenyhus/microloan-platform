from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Cleanup expired authentication tokens'

    def handle(self, *args, **options):
        # Delete tokens older than 30 days
        expired_tokens = Token.objects.filter(
            created__lt=timezone.now() - timezone.timedelta(days=30)
        )
        count = expired_tokens.count()
        expired_tokens.delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} expired tokens')
        ) 