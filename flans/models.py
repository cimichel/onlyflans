from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

class Flan(models.Model):
    
    FLAN_TYPES = [
        ("vanilla", "Vanilla Classic"),
        ("chocolate", "Chocolate Dream"),
        ("coconut", "Coconut Paradise"),
        ("coffee", "Coffee Delight"),
        ("special", "Chef's Special"),
    ]
    
    #basic flan information
    
    name = models.CharField(
        max_length=200,
        help_text="Give your flan a delicious name"
    )
    description = models.TextField(
        help_text="Describe how amazing your flan is"
    )
    
    # Using URLField for now (easier than ImageField for Day 2)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Paste a flan image URL from Unsplash"
    )
    
    # Flan characteristics
    flan_type = models.CharField(
        max_length=20,
        choices=FLAN_TYPES,
        default='vanilla'
    )
    is_premium = models.BooleanField(
        default=False,
        help_text="Check if this is premium content"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        help_text="Price for premium flans"
    )
    
    # Metadata
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='flans'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # String representation - what shows in admin
    def __str__(self):
        premium_flag = "🌟 " if self.is_premium else ""
        return f"{premium_flag}{self.name} ({self.flan_type})"
    
    # Custom method - using modern Python f-strings
    def get_display_price(self):
        return f"${self.price:.2f}" if self.is_premium else "FREE"
    
 
class Subscriber(models.Model):
    """People who want flan email updates"""
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    # Preferences
    receive_weekly_digest = models.BooleanField(default=True)
    receive_new_flan_alerts = models.BooleanField(default=True)
    favorite_flan_type = models.CharField(
        max_length=20, 
        choices=Flan.FLAN_TYPES,
        blank=True
    )
    
    def __str__(self):
        return f"{self.email} ({'Active' if self.is_active else 'Inactive'})"

class EmailLog(models.Model):
    """Track emails we send"""
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Email to {self.subscriber.email} at {self.sent_at}"   