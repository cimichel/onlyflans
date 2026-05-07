from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class FlanCreator(models.Model):
    """
    Hilarious fake creator profiles for OnlyFlans.
    Includes Gordon Hamsey, sassy grandmas, and more!
    """
    class CreatorType(models.TextChoices):
        GRANDMA = 'grandma', 'Sweet Grandma'
        CHEF = 'chef', 'Professional Chef'
        INFLUENCER = 'influencer', 'Flan Influencer'
        AMATEUR = 'amateur', 'Home Baker'

    name = models.CharField(max_length=100)
    creator_type = models.CharField(
        max_length=20,
        choices=CreatorType.choices,
        default=CreatorType.AMATEUR
    )
    bio = models.TextField(help_text="Hilarious creator biography")
    profile_image = models.URLField(max_length=500, blank=True)
    join_date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    # Fake stats for comedy
    total_earnings = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total earnings (fake stat)"
    )
    satisfaction_rate = models.IntegerField(
        default=95,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    instagram_followers = models.CharField(
        max_length=50,
        default="10K",
        help_text="Fake follower count"
    )

    class Meta:
        ordering = ['-is_featured', '-total_earnings']
        verbose_name = 'Flan Creator'
        verbose_name_plural = 'Flan Creators'

    def __str__(self) -> str:
        return f"{self.name} ({self.get_creator_type_display()})"

    @property
    def earnings_display(self) -> str:
        return f"${self.total_earnings:,.2f}"

    @property
    def is_popular(self) -> bool:
        return self.total_earnings > 1000 or self.satisfaction_rate >= 95

    @property
    def total_flans(self) -> int:
        """
        Calculated from actual DB relations — never stale.
        FIX: was a fake IntegerField that could get out of sync.
        """
        return self.flans.count()

    def get_flans_count_display(self) -> str:
        count = self.total_flans
        if count == 0:
            return "Just starting out"
        elif count == 1:
            return "1 amazing flan"
        return f"{count} incredible flans"


class Flan(models.Model):
    """
    Represents a flan dessert recipe in the OnlyFlans platform.
    """
    class FlanType(models.TextChoices):
        VANILLA = 'vanilla', 'Vanilla Classic'
        CHOCOLATE = 'chocolate', 'Chocolate Dream'
        COCONUT = 'coconut', 'Coconut Paradise'
        COFFEE = 'coffee', 'Coffee Delight'
        SPECIAL = 'special', "Chef's Special"

    # Core Information
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)

    # Categorization & Pricing
    flan_type = models.CharField(
        max_length=20,
        choices=FlanType.choices,
        default=FlanType.VANILLA,
    )
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )

    # Relationships
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='flans',
    )
    featured_creator = models.ForeignKey(
        FlanCreator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flans',  # FIX: added related_name so creator.flans.all() works
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Flan'
        verbose_name_plural = 'Flans'
        indexes = [
            models.Index(fields=['flan_type', 'is_premium']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        premium_flag = "🌟 " if self.is_premium else ""
        return f"{premium_flag}{self.name} ({self.get_flan_type_display()})"

    def get_display_price(self) -> str:
        if self.is_premium:
            return f"${self.price:.2f}"
        return "FREE"

    @property
    def short_description(self) -> str:
        if len(self.description) > 100:
            return self.description[:100] + '...'
        return self.description

    def save(self, *args, **kwargs):
        if not self.is_premium:
            self.price = Decimal('0.00')
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    """
    Represents a user subscribed to flan email updates.
    """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    receive_weekly_digest = models.BooleanField(default=True)
    receive_new_flan_alerts = models.BooleanField(default=True)
    favorite_flan_type = models.CharField(
        max_length=20,
        choices=Flan.FlanType.choices,
        blank=True,
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
        return self.name or self.email.split('@')[0]


class EmailLog(models.Model):
    """Audit log for all emails sent to subscribers."""
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name='email_logs',
    )
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=True)

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


class FlanRating(models.Model):
    """
    NEW: User ratings and reviews for flans.
    Demonstrates many-to-one relationship and unique_together constraint.
    """
    flan = models.ForeignKey(
        Flan,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 flans 🍮"
    )
    review = models.TextField(
        blank=True,
        help_text="Optional written review"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Flan Rating'
        verbose_name_plural = 'Flan Ratings'
        ordering = ['-created_at']
        # One rating per user per flan
        unique_together = [['flan', 'user']]
        indexes = [
            models.Index(fields=['flan', 'score']),
        ]

    def __str__(self) -> str:
        stars = "🍮" * self.score
        return f"{stars} {self.user.username} on '{self.flan.name}'"
