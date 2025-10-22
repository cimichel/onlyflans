from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Flan(models.Model):
    """
    Represents a flan dessert recipe in the OnlyFlans platform.

    This model stores all information about flan recipes including
    pricing, categorization, and creator information.
    """
    class FlanType(models.TextChoices):
        """Available flan types using Django's choice class"""
        VANILLA = 'vanilla', 'Vanilla Classic'
        CHOCOLATE = 'chocolate', 'Chocolate Dream'
        COCONUT = 'coconut', 'Coconut Paradise'
        COFFEE = 'coffee', 'Coffee Delight'
        SPECIAL = 'special', "Chef's Special"

    # Core Information
    name = models.CharField(
        max_length=200,
        help_text="Name of the flan recipe"
    )
    description = models.TextField(
        help_text="Detailed description of the flan"
    )
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="URL to flan image"
    )

    # Categorization & Pricing
    flan_type = models.CharField(
        max_length=20,
        choices=FlanType.choices,
        default=FlanType.VANILLA,
        help_text="Type of flan"
    )
    is_premium = models.BooleanField(
        default=False,
        help_text="Whether this is premium content"
    )
    price = models.DecimalField(
        max_digits=6,  # 9999.99
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price for premium flans"
    )

    # Relationships
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='flans',  # user.flans.all() works now!
        help_text="User who created this flan"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata"""
        ordering = ['-created_at']  # Newest first by default
        verbose_name = 'Flan'
        verbose_name_plural = 'Flans'
        indexes = [
            models.Index(fields=['flan_type', 'is_premium']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        """String representation"""
        premium_flag = "🌟 " if self.is_premium else ""
        return f"{premium_flag}{self.name} ({self.get_flan_type_display()})"

    def get_display_price(self) -> str:
        """Get formatted price for display"""
        if self.is_premium:
            return f"${self.price:.2f}"
        return "FREE"

    @property
    def short_description(self) -> str:
        """Get truncated description for previews"""
        if len(self.description) > 100:
            return self.description[:100] + '...'
        return self.description

    def save(self, *args, **kwargs):
        """Custom save logic"""
        # Ensure free flans have price 0
        if not self.is_premium:
            self.price = Decimal('0.00')
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    """
    Represents a user subscribed to flan email updates.

    Stores subscriber preferences and contact information
    for email marketing and notifications.
    """
    email = models.EmailField(
        unique=True,
        help_text="Subscriber's email address"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Subscriber's name (optional)"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the subscriber is active"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    # Preferences
    receive_weekly_digest = models.BooleanField(
        default=True,
        help_text="Receive weekly flan digest emails"
    )
    receive_new_flan_alerts = models.BooleanField(
        default=True,
        help_text="Receive alerts for new flans"
    )
    favorite_flan_type = models.CharField(
        max_length=20,
        choices=Flan.FlanType.choices,
        blank=True,
        help_text="Favorite flan type for personalized content"
    )

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        ordering = ['-subscribed_at']

    def __str__(self) -> str:
        status = "Active" if self.is_active else "Inactive"
        return f"{self.email} ({status})"

    @property
    def display_name(self) -> str:
        """Get display name (name or email)"""
        return self.name or self.email.split('@')[0]


class EmailLog(models.Model):
    """
    Audit log for all emails sent to subscribers.

    Tracks email delivery for analytics and debugging purposes.
    """
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name='email_logs',
        help_text="Subscriber who received the email"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Email subject line"
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(
        default=True,
        help_text="Whether the email was sent successfully"
    )

    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sent_at']),
            models.Index(fields=['was_successful']),
        ]

    def __str__(self) -> str:
        status = "✅" if self.was_successful else "❌"
        return f"{status} Email to {self.subscriber.email} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
