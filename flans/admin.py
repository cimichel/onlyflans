from django.contrib import admin
from .models import Flan, Subscriber, EmailLog

# Register your models here.
from .models import Flan

# Customize how Flan appears in admin


class FlanAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['name', 'flan_type', 'is_premium',
                    'price', 'creator', 'created_at']

    # Filter options in the right sidebar
    list_filter = ['flan_type', 'is_premium', 'created_at']

    # Search functionality
    search_fields = ['name', 'description']

    # Pre-populate fields (if we had slugs)
    # prepopulated_fields = {"slug": ("name",)}

    # Fieldsets for organized form display
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'flan_type')
        }),
        ('Media & Pricing', {
            'fields': ('image_url', 'is_premium', 'price')
        }),
        ('Ownership', {
            'fields': ('creator',)
        }),
    )


# Register your model with the custom admin
admin.site.register(Flan, FlanAdmin)

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'favorite_flan_type']
    list_filter = ['is_active', 'receive_weekly_digest', 'favorite_flan_type']
    search_fields = ['email', 'name']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'subject', 'sent_at', 'was_successful']
    list_filter = ['was_successful', 'sent_at']
    readonly_fields = ['sent_at']