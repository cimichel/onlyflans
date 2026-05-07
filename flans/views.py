from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count

from .models import Flan, FlanCreator, FlanRating
from .services import FlanService, SubscriberService, AnalyticsService
from .datatypes import FlanCreateData
from .exceptions import FlanNotFoundError
import logging

logger = logging.getLogger(__name__)

FLANS_PER_PAGE = 9


def flan_list(request: HttpRequest) -> HttpResponse:
    """
    Display all flans with filtering and pagination.

    FIX: Added pagination — loading all flans at once doesn't scale.
    FIX: Uses ORM aggregate for stats instead of Python loops.
    """
    try:
        flan_type = request.GET.get('type', '')
        page_number = request.GET.get('page', 1)

        # Filter queryset
        queryset = Flan.objects.select_related('featured_creator', 'creator')
        if flan_type:
            queryset = queryset.filter(flan_type=flan_type)

        # Paginate
        paginator = Paginator(queryset, FLANS_PER_PAGE)
        page_obj = paginator.get_page(page_number)

        # FIX: Single DB query for stats instead of Python sum() loop
        system_analytics = AnalyticsService.get_system_analytics()

        context: Dict[str, Any] = {
            'flans': page_obj,
            'page_obj': page_obj,
            'selected_type': flan_type,
            # FIX: was Flan.FLAN_TYPES (didn't exist)
            'flan_types': Flan.FlanType.choices,
            'total_flans': paginator.count,
            'system_analytics': system_analytics,
        }

        return render(request, 'flans/list.html', context)

    except Exception as e:
        logger.error(f"Error in flan_list view: {e}")
        messages.error(request, "An error occurred while loading flans.")
        return render(request, 'flans/list.html', {
            'flans': [],
            'flan_types': Flan.FlanType.choices,
            'system_analytics': {}
        })


def flan_detail(request: HttpRequest, flan_id: int) -> HttpResponse:
    """
    Display detailed view of a single flan.

    FIX: Was querying the DB twice (service + ORM). Now one query.
    NEW: Shows ratings and handles rating submission.
    """
    flan = get_object_or_404(
        Flan.objects.select_related('creator', 'featured_creator'),
        id=flan_id
    )

    # Get rating stats in one query
    rating_stats = flan.ratings.aggregate(
        avg_score=Avg('score'),
        total_ratings=Count('id'),
    )

    # Check if current user has rated this flan
    user_rating = None
    if request.user.is_authenticated:
        user_rating = flan.ratings.filter(user=request.user).first()

    context = {
        'flan': flan,
        'display_type': flan.get_flan_type_display(),
        'display_price': flan.get_display_price(),
        'avg_score': round(rating_stats['avg_score'] or 0, 1),
        'total_ratings': rating_stats['total_ratings'],
        'user_rating': user_rating,
        'score_range': range(1, 6),  # for rendering 5 stars in template
    }

    return render(request, 'flans/detail.html', context)


@login_required
def rate_flan(request: HttpRequest, flan_id: int) -> HttpResponse:
    """
    NEW: Handle flan rating submission.
    Uses update_or_create — one query, no race conditions.
    """
    if request.method != 'POST':
        return redirect('flan-detail', flan_id=flan_id)

    flan = get_object_or_404(Flan, id=flan_id)

    try:
        score = int(request.POST.get('score', 0))
        review = request.POST.get('review', '').strip()

        if not 1 <= score <= 5:
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect('flan-detail', flan_id=flan_id)

        # update_or_create: if rating exists update it, otherwise create it
        rating, created = FlanRating.objects.update_or_create(
            flan=flan,
            user=request.user,
            defaults={'score': score, 'review': review}
        )

        action = "submitted" if created else "updated"
        messages.success(
            request, f"Your rating has been {action}! {'🍮' * score}")
        logger.info(
            f"User {request.user.username} {action} rating for flan {flan_id}")

    except (ValueError, TypeError):
        messages.error(request, "Invalid rating value.")
    except Exception as e:
        logger.error(f"Error in rate_flan view: {e}")
        messages.error(
            request, "An error occurred while submitting your rating.")

    return redirect('flan-detail', flan_id=flan_id)


def subscribe(request: HttpRequest) -> HttpResponse:
    """Handle newsletter subscriptions using service layer."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()

        if not email:
            messages.error(request, "Email address is required.")
            return redirect('flan-list')

        try:
            success, subscriber_data, message = SubscriberService.create_subscriber(
                email, name
            )
            if success:
                messages.success(request, message)
                logger.info(f"New subscriber: {email}")
            else:
                messages.info(request, message)

        except Exception as e:
            logger.error(f"Error in subscribe view: {e}")
            messages.error(request, "An error occurred during subscription.")

        return redirect('flan-list')

    return redirect('flan-list')


def faq(request: HttpRequest) -> HttpResponse:
    """FAQ page."""
    return render(request, 'flans/faq.html')


@login_required
def create_flan(request: HttpRequest) -> HttpResponse:
    """Create a new flan (login required)."""
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
            flan_data, request.user
        )

        if success:
            messages.success(request, f"Flan '{created_flan.name}' created! 🍮")
            return redirect('flan-detail', flan_id=created_flan.id)
        else:
            for error in errors:
                messages.error(request, error)

    return render(request, 'flans/create_flan.html', {
        'flan_types': Flan.FlanType.choices  # FIX: was Flan.FLAN_TYPES
    })


def creators_list(request: HttpRequest) -> HttpResponse:
    """
    Display all flan creators.

    FIX: Uses DB aggregation instead of Python loops for stats.
    FIX: Uses select_related to avoid N+1 queries.
    """
    try:
        creators = FlanCreator.objects.prefetch_related('flans')

        # FIX: One DB query instead of Python sum() loop
        stats = creators.aggregate(
            total_earnings=Sum('total_earnings'),
            avg_satisfaction=Avg('satisfaction_rate'),
        )

        context = {
            'creators': creators,
            'featured_creators': creators.filter(is_featured=True),
            'grandma_creators': creators.filter(creator_type='grandma'),
            'chef_creators': creators.filter(creator_type='chef'),
            'influencer_creators': creators.filter(creator_type='influencer'),
            'total_creators': creators.count(),
            'total_earnings': stats['total_earnings'] or 0,
            'avg_satisfaction': round(stats['avg_satisfaction'] or 0, 1),
        }

        return render(request, 'flans/creators.html', context)

    except Exception as e:
        logger.error(f"Error in creators_list view: {e}")
        messages.error(request, "An error occurred while loading creators.")
        return render(request, 'flans/creators.html', {'creators': []})


def creator_detail(request: HttpRequest, creator_id: int) -> HttpResponse:
    """
    Display detailed view of a creator.

    FIX: Was returning random Flan.objects.all()[:3] as mock data.
    Now returns actual flans linked to this creator via FK.
    """
    creator = get_object_or_404(FlanCreator, id=creator_id)

    # FIX: actual related flans via featured_creator FK
    creator_flans = Flan.objects.filter(
        featured_creator=creator
    ).select_related('creator')

    context = {
        'creator': creator,
        'creator_flans': creator_flans,
        'is_popular': creator.is_popular,
        'flans_count_display': creator.get_flans_count_display(),
    }

    return render(request, 'flans/creator_detail.html', context)
