from django.core.management.base import BaseCommand
from flans.services import FlanService, SubscriberService
from flans.datatypes import FlanCreateData
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test the new service classes and dataclasses'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testing Service Classes...')

        # Test FlanService
        flans = FlanService.get_all_flans()
        self.stdout.write(f'📊 Found {len(flans)} flans')

        if flans:
            first_flan = flans[0]
            self.stdout.write(f'🍮 First flan: {first_flan.name}')
            self.stdout.write(f'💰 Price: {first_flan.display_price}')

        # Test SubscriberService
        sub_count = SubscriberService.get_active_subscribers_count()
        self.stdout.write(f'📧 Active subscribers: {sub_count}')

        # Test AnalyticsService
        from flans.services import AnalyticsService
        analytics = AnalyticsService.get_system_analytics()
        self.stdout.write(f'📈 System analytics: {analytics}')

        self.stdout.write(self.style.SUCCESS(
            '✅ All services working correctly!'))
