from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User

@dataclass
class FlanData:
    """Clean data structure - immutable and type-safe"""
    name: str
    description: str
    image_url: str
    flan_type: str
    is_premium: bool
    price: Decimal
    creator_id: int
    created_at: Optional[datetime] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'flan_type': self.flan_type,
            'is_premium': self.is_premium,
            'price': float(self.price),  # Convert for JSON serialization
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_model(cls, flan_model) -> 'FlanData':
        """Create FlanData from Django model instance"""
        return cls(
            id=flan_model.id,
            name=flan_model.name,
            description=flan_model.description,
            image_url=flan_model.image_url,
            flan_type=flan_model.flan_type,
            is_premium=flan_model.is_premium,
            price=flan_model.price,
            creator_id=flan_model.creator.id,
            created_at=flan_model.created_at
        )
    
    @property
    def display_price(self) -> str:
        """Formatted price for display"""
        if self.is_premium:
            return f"${self.price:.2f}"
        return "FREE"

@dataclass
class FlanCreateData:
    """Data structure for creating new flans (input validation)"""
    name: str
    description: str
    image_url: str
    flan_type: str
    is_premium: bool = False
    price: Decimal = Decimal('0.00')
    
    def validate(self) -> List[str]:
        """Validate flan data before creation"""
        errors = []
        if len(self.name) < 3:
            errors.append("Name must be at least 3 characters")
        if len(self.description) < 10:
            errors.append("Description must be at least 10 characters")
        if self.is_premium and self.price <= 0:
            errors.append("Premium flans must have a positive price")
        if self.flan_type not in ['vanilla', 'chocolate', 'coconut', 'coffee', 'special']:
            errors.append("Invalid flan type")
        return errors

@dataclass
class SubscriberData:
    """Data structure for subscriber information"""
    email: str
    name: str = ""
    is_active: bool = True
    receive_weekly_digest: bool = True
    receive_new_flan_alerts: bool = True
    favorite_flan_type: str = ""
    subscribed_at: Optional[datetime] = None
    id: Optional[int] = None
    
    @classmethod
    def from_model(cls, subscriber_model) -> 'SubscriberData':
        return cls(
            id=subscriber_model.id,
            email=subscriber_model.email,
            name=subscriber_model.name,
            is_active=subscriber_model.is_active,
            receive_weekly_digest=subscriber_model.receive_weekly_digest,
            receive_new_flan_alerts=subscriber_model.receive_new_flan_alerts,
            favorite_flan_type=subscriber_model.favorite_flan_type,
            subscribed_at=subscriber_model.subscribed_at
        )

@dataclass
class EmailTemplateData:
    """Data structure for email templates with validation"""
    template_name: str
    subject: str
    context: Dict = field(default_factory=dict)
    recipient_email: str = ""
    from_email: str = 'noreply@onlyflans.com'
    
    def validate_context(self) -> bool:
        """Validate that required context keys are present"""
        required_keys = ['subscriber', 'site_url']
        return all(key in self.context for key in required_keys)
    
    def get_required_context_keys(self) -> List[str]:
        """Get list of missing required context keys"""
        required_keys = ['subscriber', 'site_url']
        return [key for key in required_keys if key not in self.context]

@dataclass
class AnalyticsData:
    """Data structure for flan analytics and metrics"""
    flan_id: int
    views_count: int = 0
    likes_count: int = 0
    subscription_count: int = 0
    revenue: Decimal = Decimal('0.00')
    created_at: datetime = field(default_factory=datetime.now)
    
    @property
    def engagement_rate(self) -> float:
        """Calculate engagement rate as percentage"""
        if self.views_count == 0:
            return 0.0
        return round((self.likes_count / self.views_count) * 100, 2)
    
    @property
    def revenue_per_subscription(self) -> Decimal:
        """Calculate average revenue per subscription"""
        if self.subscription_count == 0:
            return Decimal('0.00')
        return round(self.revenue / self.subscription_count, 2)
    
    def to_dict(self) -> Dict:
        """Convert analytics to dictionary for API responses"""
        return {
            'flan_id': self.flan_id,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'subscription_count': self.subscription_count,
            'revenue': float(self.revenue),
            'engagement_rate': self.engagement_rate,
            'revenue_per_subscription': float(self.revenue_per_subscription),
            'created_at': self.created_at.isoformat()
        }

@dataclass
class PaginatedResponse:
    """Generic paginated response structure"""
    data: List
    total_count: int
    page: int
    page_size: int
    total_pages: int
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        return self.page > 1
    
    def to_dict(self) -> Dict:
        return {
            'data': [item.to_dict() if hasattr(item, 'to_dict') else item for item in self.data],
            'pagination': {
                'total_count': self.total_count,
                'page': self.page,
                'page_size': self.page_size,
                'total_pages': self.total_pages,
                'has_next': self.has_next,
                'has_previous': self.has_previous
            }
        }