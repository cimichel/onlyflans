from django.contrib import admin

# Register your models here.
from .models import Flan

# Customize how Flan appears in admin
class FlanAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['name', 'flan_type', 'is_premium', 'price', 'creator', 'created_at']
    
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