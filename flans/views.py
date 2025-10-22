from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from .models import Flan
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Subscriber
from django.contrib.auth.decorators import login_required

from .models import Flan
from .services import FlanService, SubscriberService, AnalyticsService
from .datatypes import FlanCreateData
from .exceptions import FlanNotFoundError, DuplicateSubscriberError
import logging

logger = logging.getLogger(__name__)


def flan_list(request: HttpRequest) -> HttpResponse:
    """Display all flans with filtering options using service layer"""
    try:
        flan_type = request.GET.get('type', '')

        # Use service to get flans
        if flan_type:
            flan_data_list = FlanService.get_flans_by_type(flan_type)
        else:
            flan_data_list = FlanService.get_all_flans()

        # Get system analytics for the stats bar
        system_analytics = AnalyticsService.get_system_analytics()

        context: Dict[str, Any] = {
            'flans': flan_data_list,
            'selected_type': flan_type,
            'total_flans': len(flan_data_list),
            'system_analytics': system_analytics
        }

        return render(request, 'flans/list.html', context)

    except Exception as e:
        logger.error(f"Error in flan_list view: {e}")
        messages.error(request, "An error occurred while loading flans.")
        return render(request, 'flans/list.html', {'flans': [], 'system_analytics': {}})


def flan_detail(request: HttpRequest, flan_id: int) -> HttpResponse:
    """Display detailed view of a single flan using service layer"""
    try:
        # Use service to get flan data
        flan_data = FlanService.get_flan_by_id(flan_id)
        analytics = FlanService.get_flan_analytics(flan_id)

        # Get the actual model for template compatibility
        flan_model = Flan.objects.get(id=flan_id)

        context = {
            'flan': flan_model,  # Keep model for template compatibility
            'flan_data': flan_data,  # New: pass dataclass too
            'display_type': flan_model.get_flan_type_display(),
            'display_price': flan_model.get_display_price(),
            'analytics': analytics
        }

        return render(request, 'flans/detail.html', context)

    except FlanNotFoundError:
        messages.error(request, "Flan not found.")
        return redirect('flan-list')
    except Exception as e:
        logger.error(f"Error in flan_detail view for flan {flan_id}: {e}")
        messages.error(
            request, "An error occurred while loading the flan details.")
        return redirect('flan-list')


def subscribe(request: HttpRequest) -> HttpResponse:
    """Handle newsletter subscriptions using service layer"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()

        if not email:
            messages.error(request, "Email address is required.")
            return redirect('flan-list')

        try:
            # Use service to create subscriber
            success, subscriber_data, message = SubscriberService.create_subscriber(
                email, name)

            if success:
                messages.success(request, message)
                logger.info(f"New subscriber: {email}")
            else:
                # Use info for duplicate subscriptions
                messages.info(request, message)

        except Exception as e:
            logger.error(f"Error in subscribe view: {e}")
            messages.error(request, "An error occurred during subscription.")

        return redirect('flan-list')

    # GET request - redirect to flan list
    return redirect('flan-list')


def faq(request: HttpRequest) -> HttpResponse:
    """FAQ page"""
    return render(request, 'flans/faq.html')

# New view for demonstration


@login_required
def create_flan(request: HttpRequest) -> HttpResponse:
    """Demo view for creating flans using service layer (protected)"""
    if request.method == 'POST':
        flan_data = FlanCreateData(
            name=request.POST.get('name', ''),
            description=request.POST.get('description', ''),
            image_url=request.POST.get('image_url', ''),
            flan_type=request.POST.get('flan_type', 'vanilla'),
            is_premium=bool(request.POST.get('is_premium', False)),
            price=request.POST.get('price', '0.00')
        )

        success, created_flan, errors = FlanService.create_flan(
            flan_data, request.user)

        if success:
            messages.success(
                request, f"Flan '{created_flan.name}' created successfully!")
            return redirect('flan-detail', flan_id=created_flan.id)
        else:
            for error in errors:
                messages.error(request, error)

    # GET request or failed POST - show form
    return render(request, 'flans/create_flan.html', {
        'flan_types': Flan.FLAN_TYPES
    })
