from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Subscriber, EmailLog


def send_weekly_digest():
    """Send weekly flan digest to all active subscribers"""
    subscribers = Subscriber.objects.filter(
        is_active=True, receive_weekly_digest=True)

    # Get flan data for the email
    from .models import Flan
    from django.utils import timezone
    from datetime import timedelta

    # Flans from the last 7 days
    last_week = timezone.now() - timedelta(days=7)
    recent_flans = Flan.objects.filter(created_at__gte=last_week)[:3]

    # Stats for the email
    new_flans_count = Flan.objects.filter(created_at__gte=last_week).count()
    premium_count = Flan.objects.filter(
        created_at__gte=last_week, is_premium=True).count()

    # Most popular flan type this week (simplified)
    from django.db.models import Count
    popular_type = Flan.objects.filter(created_at__gte=last_week).values(
        'flan_type').annotate(count=Count('id')).order_by('-count').first()
    most_popular_type = popular_type['flan_type'] if popular_type else "Vanilla"

    for subscriber in subscribers:
        subject = f"🍮 Your Weekly Flan Digest - {new_flans_count} New Flans!"

        try:
            # Dynamic context for each subscriber
            context = {
                'subscriber': subscriber,
                'featured_flans': recent_flans,
                'new_flans_count': new_flans_count,
                'premium_count': premium_count,
                'most_popular_type': most_popular_type,
                'site_url': 'http://localhost:8000',
                'unsubscribe_url': f'http://localhost:8000/unsubscribe/{subscriber.id}/'
            }

            # FIX: Use the correct template path
            html_content = render_to_string(
                'flans/emails/weekly_digest.html', context)
            text_content = strip_tags(html_content)

            # Create email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email]
            )
            email.attach_alternative(html_content, "text/html")

            # Send email
            email.send()

            # Log the email
            EmailLog.objects.create(
                subscriber=subscriber,
                subject=subject,
                was_successful=True
            )

            print(f"✅ Sent weekly digest to {subscriber.email}")

        except Exception as e:
            print(f"❌ Failed to send to {subscriber.email}: {e}")
            EmailLog.objects.create(
                subscriber=subscriber,
                subject=subject,
                was_successful=False
            )


def send_new_flan_alert(flan):
    """Send alert about a new flan to interested subscribers"""
    subscribers = Subscriber.objects.filter(
        is_active=True,
        receive_new_flan_alerts=True
    )

    subject = f"🍮 New Flan Alert: {flan.name}"

    for subscriber in subscribers:
        if subscriber.favorite_flan_type and subscriber.favorite_flan_type != flan.flan_type:
            continue

        try:
            context = {
                'subscriber': subscriber,
                'flan': flan,
                'site_url': 'http://localhost:8000',
                'unsubscribe_url': f'http://localhost:8000/unsubscribe/{subscriber.id}/'
            }

            # FIX: Use the correct template path
            html_content = render_to_string(
                'flans/emails/new_flan_alert.html', context)
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            EmailLog.objects.create(
                subscriber=subscriber,
                subject=subject,
                was_successful=True
            )

            print(f"✅ Sent new flan alert to {subscriber.email}")

        except Exception as e:
            print(f"❌ Failed to send alert to {subscriber.email}: {e}")
            EmailLog.objects.create(
                subscriber=subscriber,
                subject=subject,
                was_successful=False
            )
