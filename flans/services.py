from typing import List, Optional, Dict, Tuple
from decimal import Decimal
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .models import Flan, Subscriber
from .datatypes import FlanData, FlanCreateData, AnalyticsData, PaginatedResponse, SubscriberData
from .exceptions import FlanNotFoundError, InvalidFlanDataError, DuplicateSubscriberError
import logging

logger = logging.getLogger(__name__)

class FlanService:
    """Service class for flan-related business logic"""
    
    @staticmethod
    def get_all_flans() -> List[FlanData]:
        """Get all flans as FlanData objects"""
        try:
            flans = Flan.objects.select_related('creator').all()
            return [FlanData.from_model(flan) for flan in flans]
        except Exception as e:
            logger.error(f"Error getting all flans: {e}")
            return []
    
    @staticmethod
    def get_flans_by_type(flan_type: Optional[str] = None) -> List[FlanData]:
        """Get flans filtered by type"""
        try:
            queryset = Flan.objects.select_related('creator').all()
            if flan_type:
                queryset = queryset.filter(flan_type=flan_type)
            
            return [FlanData.from_model(flan) for flan in queryset]
        except Exception as e:
            logger.error(f"Error getting flans by type {flan_type}: {e}")
            return []
    
    @staticmethod
    def get_flan_by_id(flan_id: int) -> Optional[FlanData]:
        """Get a specific flan by ID"""
        try:
            flan = Flan.objects.select_related('creator').get(id=flan_id)
            return FlanData.from_model(flan)
        except Flan.DoesNotExist:
            logger.warning(f"Flan with id {flan_id} not found")
            raise FlanNotFoundError(flan_id)
        except Exception as e:
            logger.error(f"Error getting flan {flan_id}: {e}")
            return None
    
    @staticmethod
    def get_premium_flans() -> List[FlanData]:
        """Get all premium flans"""
        try:
            flans = Flan.objects.select_related('creator').filter(is_premium=True)
            return [FlanData.from_model(flan) for flan in flans]
        except Exception as e:
            logger.error(f"Error getting premium flans: {e}")
            return []
    
    @staticmethod
    def create_flan(flan_data: FlanCreateData, creator: User) -> Tuple[bool, FlanData, List[str]]:
        """Create a new flan with validation"""
        # Validate input data
        errors = flan_data.validate()
        if errors:
            return False, None, errors
        
        try:
            flan = Flan.objects.create(
                name=flan_data.name,
                description=flan_data.description,
                image_url=flan_data.image_url,
                flan_type=flan_data.flan_type,
                is_premium=flan_data.is_premium,
                price=flan_data.price,
                creator=creator
            )
            
            flan_data_out = FlanData.from_model(flan)
            logger.info(f"Created new flan: {flan_data.name}")
            return True, flan_data_out, []
            
        except Exception as e:
            logger.error(f"Error creating flan {flan_data.name}: {e}")
            return False, None, [f"Database error: {str(e)}"]
    
    @staticmethod
    def get_flan_analytics(flan_id: int) -> Optional[AnalyticsData]:
        """Get analytics for a specific flan"""
        try:
            # Verify flan exists
            flan = Flan.objects.get(id=flan_id)
            
            # Mock analytics data - in real app, this would come from actual tracking
            # This demonstrates the pattern without requiring additional infrastructure
            return AnalyticsData(
                flan_id=flan.id,
                views_count=100 + (flan.id * 10),  # Mock data based on ID
                likes_count=25 + (flan.id * 5),    # Mock data
                subscription_count=10 + flan.id,   # Mock data
                revenue=Decimal(str(49.90 + (flan.id * 5)))  # Mock data
            )
        except Flan.DoesNotExist:
            logger.warning(f"Flan with id {flan_id} not found for analytics")
            raise FlanNotFoundError(flan_id)
        except Exception as e:
            logger.error(f"Error getting analytics for flan {flan_id}: {e}")
            return None
    
    @staticmethod
    def get_flans_paginated(page: int = 1, page_size: int = 10) -> PaginatedResponse:
        """Get paginated flans"""
        try:
            flans_queryset = Flan.objects.select_related('creator').all().order_by('-created_at')
            paginator = Paginator(flans_queryset, page_size)
            
            page_obj = paginator.get_page(page)
            flan_data_list = [FlanData.from_model(flan) for flan in page_obj.object_list]
            
            return PaginatedResponse(
                data=flan_data_list,
                total_count=paginator.count,
                page=page,
                page_size=page_size,
                total_pages=paginator.num_pages
            )
        except Exception as e:
            logger.error(f"Error getting paginated flans: {e}")
            # Return empty paginated response
            return PaginatedResponse(
                data=[],
                total_count=0,
                page=page,
                page_size=page_size,
                total_pages=0
            )

class SubscriberService:
    """Service class for subscriber operations"""
    
    @staticmethod
    def get_active_subscribers_count() -> int:
        """Get count of active subscribers"""
        return Subscriber.objects.filter(is_active=True).count()
    
    @staticmethod
    def get_subscribers_by_preference() -> Dict[str, int]:
        """Get subscriber counts by preference"""
        return {
            'weekly_digest': Subscriber.objects.filter(receive_weekly_digest=True).count(),
            'new_flan_alerts': Subscriber.objects.filter(receive_new_flan_alerts=True).count(),
            'total_active': Subscriber.objects.filter(is_active=True).count()
        }
    
    @staticmethod
    def create_subscriber(email: str, name: str = "") -> Tuple[bool, SubscriberData, str]:
        """Create a new subscriber with duplicate checking"""
        try:
            # Check for existing subscriber
            if Subscriber.objects.filter(email=email).exists():
                raise DuplicateSubscriberError(email)
            
            subscriber = Subscriber.objects.create(
                email=email,
                name=name,
                is_active=True
            )
            
            subscriber_data = SubscriberData.from_model(subscriber)
            logger.info(f"Created new subscriber: {email}")
            return True, subscriber_data, "Subscribed successfully!"
            
        except DuplicateSubscriberError as e:
            logger.warning(f"Duplicate subscriber attempt: {email}")
            return False, None, str(e)
        except Exception as e:
            logger.error(f"Error creating subscriber {email}: {e}")
            return False, None, f"Subscription failed: {str(e)}"
    
    @staticmethod
    def get_subscribers_for_weekly_digest() -> List[SubscriberData]:
        """Get all active subscribers who want weekly digest"""
        try:
            subscribers = Subscriber.objects.filter(
                is_active=True, 
                receive_weekly_digest=True
            )
            return [SubscriberData.from_model(sub) for sub in subscribers]
        except Exception as e:
            logger.error(f"Error getting subscribers for digest: {e}")
            return []

class AnalyticsService:
    """Service class for analytics and reporting"""
    
    @staticmethod
    def get_system_analytics() -> Dict:
        """Get overall system analytics"""
        try:
            total_flans = Flan.objects.count()
            premium_flans = Flan.objects.filter(is_premium=True).count()
            total_subscribers = Subscriber.objects.filter(is_active=True).count()
            
            # Mock revenue calculation
            total_revenue = Flan.objects.filter(is_premium=True).aggregate(
                total=Sum('price')
            )['total'] or Decimal('0.00')
            
            return {
                'total_flans': total_flans,
                'premium_flans': premium_flans,
                'free_flans': total_flans - premium_flans,
                'total_subscribers': total_subscribers,
                'total_revenue': float(total_revenue),
                'avg_flan_price': float(
                    Flan.objects.filter(is_premium=True).aggregate(
                        avg=Avg('price')
                    )['avg'] or Decimal('0.00')
                ),
                'premium_conversion_rate': round(
                    (premium_flans / total_flans * 100) if total_flans > 0 else 0, 
                    2
                )
            }
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return {}