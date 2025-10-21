from django.db import models
from django.contrib.auth.models import User

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