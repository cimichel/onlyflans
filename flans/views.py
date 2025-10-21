from django.shortcuts import render, get_object_or_404, redirect
from .models import Flan
from django.contrib import messages
from .models import Subscriber


def flan_list(request):
    """Display all flans with filtering options"""
    flan_type = request.GET.get('type', '')

    # Using Django ORM filtering (interview concept!)
    if flan_type:
        flans = Flan.objects.filter(flan_type=flan_type)
    else:
        flans = Flan.objects.all()

    # Using list comprehension with conditional (modern Python)
    flan_data = [{
        'id': flan.id,
        'name': flan.name,
        # Truncate long descriptions
        'description': flan.description[:100] + '...' if len(flan.description) > 100 else flan.description,
        'image_url': flan.image_url,
        'type': flan.get_flan_type_display(),
        'price': flan.get_display_price(),
        'is_premium': flan.is_premium
    } for flan in flans]

    context = {
        'flans': flan_data,
        'selected_type': flan_type,
        # Using len() instead of count() since we already have the queryset
        'total_flans': len(flans)
    }

    return render(request, 'flans/list.html', context)


def flan_detail(request, flan_id):
    """Display detailed view of a single flan"""
    # get_object_or_404 is Django shortcut - tries to get object, returns 404 if not found
    flan = get_object_or_404(Flan, id=flan_id)

    context = {
        'flan': flan,
        'display_type': flan.get_flan_type_display(),  # Human-readable choice
        'display_price': flan.get_display_price(),
    }

    return render(request, 'flans/detail.html', context)


def faq(request):
    return render(request, 'flans/faq.html')


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name', '')

        try:
            # Create or update subscriber
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'name': name, 'is_active': True}
            )

            if created:
                messages.success(
                    request, f"🎉 Welcome to the Flan Family, {name or email}! You'll get weekly flan updates.")
            else:
                messages.info(
                    request, f"You're already subscribed with {email}!")

        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")

        return redirect('flan-list')
