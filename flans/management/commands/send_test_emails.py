from django.core.management.base import BaseCommand
from flans.models import Subscriber
from flans.emails import send_weekly_digest

class Command(BaseCommand):
    help = 'Send test weekly digest email'
    
    def handle(self, *args, **options):
        # Create a test subscriber if none exists
        if not Subscriber.objects.exists():
            Subscriber.objects.create(
                email='test@example.com',
                name='Test User',
                is_active=True
            )
            self.stdout.write('✅ Created test subscriber')
        
        # Send weekly digest
        send_weekly_digest()
        self.stdout.write('✅ Test emails sent! Check your console for output.')