from rest_framework import serializers
from .models import Flan, FlanCreator, FlanRating, Subscriber


class FlanCreatorSerializer(serializers.ModelSerializer):
    total_flans = serializers.ReadOnlyField()  # computed property
    earnings_display = serializers.ReadOnlyField()

    class Meta:
        model = FlanCreator
        fields = [
            'id', 'name', 'creator_type', 'bio',
            'profile_image', 'join_date', 'is_featured',
            'total_flans', 'total_earnings', 'earnings_display',
            'satisfaction_rate', 'instagram_followers', 'is_popular',
        ]


class FlanRatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    stars = serializers.SerializerMethodField()

    class Meta:
        model = FlanRating
        fields = ['id', 'username', 'score', 'stars', 'review', 'created_at']

    def get_stars(self, obj) -> str:
        return "🍮" * obj.score


class FlanListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — no nested objects."""
    display_price = serializers.ReadOnlyField(source='get_display_price')
    flan_type_display = serializers.ReadOnlyField(
        source='get_flan_type_display')
    short_description = serializers.ReadOnlyField()

    class Meta:
        model = Flan
        fields = [
            'id', 'name', 'flan_type', 'flan_type_display',
            'short_description', 'image_url', 'is_premium',
            'display_price', 'created_at',
        ]


class FlanDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views — includes nested creator and ratings."""
    display_price = serializers.ReadOnlyField(source='get_display_price')
    flan_type_display = serializers.ReadOnlyField(
        source='get_flan_type_display')
    featured_creator = FlanCreatorSerializer(read_only=True)
    ratings = FlanRatingSerializer(many=True, read_only=True)
    avg_score = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()

    class Meta:
        model = Flan
        fields = [
            'id', 'name', 'description', 'flan_type', 'flan_type_display',
            'image_url', 'is_premium', 'display_price', 'price',
            'featured_creator', 'ratings', 'avg_score', 'total_ratings',
            'created_at', 'updated_at',
        ]

    def get_avg_score(self, obj) -> float:
        from django.db.models import Avg
        result = obj.ratings.aggregate(avg=Avg('score'))
        return round(result['avg'] or 0, 1)

    def get_total_ratings(self, obj) -> int:
        return obj.ratings.count()


class SubscribeSerializer(serializers.ModelSerializer):
    """For the subscription API endpoint."""
    class Meta:
        model = Subscriber
        fields = ['email', 'name', 'favorite_flan_type',
                  'receive_weekly_digest', 'receive_new_flan_alerts']

    def validate_email(self, value: str) -> str:
        return value.lower().strip()
