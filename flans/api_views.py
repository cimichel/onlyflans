from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Avg, Count

from .models import Flan, FlanCreator, FlanRating
from .serializers import (
    FlanListSerializer, FlanDetailSerializer,
    FlanCreatorSerializer, FlanRatingSerializer,
    SubscribeSerializer,
)


class FlanListAPIView(generics.ListAPIView):
    """
    GET /api/flans/
    Returns paginated list of all flans.
    Supports filtering by type: /api/flans/?type=chocolate
    Supports ordering: /api/flans/?ordering=-created_at
    """
    serializer_class = FlanListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'price', 'name']
    ordering = ['-created_at']
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Flan.objects.select_related('featured_creator', 'creator')
        flan_type = self.request.query_params.get('type')
        is_premium = self.request.query_params.get('premium')

        if flan_type:
            queryset = queryset.filter(flan_type=flan_type)
        if is_premium is not None:
            queryset = queryset.filter(is_premium=is_premium.lower() == 'true')

        return queryset


class FlanDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/flans/<id>/
    Returns full flan details including creator and ratings.
    """
    queryset = Flan.objects.select_related(
        'creator', 'featured_creator'
    ).prefetch_related('ratings__user')
    serializer_class = FlanDetailSerializer
    permission_classes = [AllowAny]


class FlanCreatorListAPIView(generics.ListAPIView):
    """
    GET /api/creators/
    Returns all flan creators. Featured creators first.
    """
    queryset = FlanCreator.objects.prefetch_related('flans')
    serializer_class = FlanCreatorSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_earnings', 'satisfaction_rate']
    ordering = ['-is_featured', '-total_earnings']


class FlanRatingListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/flans/<flan_id>/ratings/  — list ratings for a flan
    POST /api/flans/<flan_id>/ratings/  — submit or update a rating (auth required)
    """
    serializer_class = FlanRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return FlanRating.objects.filter(
            flan_id=self.kwargs['flan_id']
        ).select_related('user')

    def create(self, request: Request, *args, **kwargs) -> Response:
        flan_id = self.kwargs['flan_id']
        score = request.data.get('score')
        review = request.data.get('review', '')

        try:
            score = int(score)
            if not 1 <= score <= 5:
                return Response(
                    {'error': 'Score must be between 1 and 5.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError):
            return Response(
                {'error': 'Invalid score value.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        flan = generics.get_object_or_404(Flan, id=flan_id)

        rating, created = FlanRating.objects.update_or_create(
            flan=flan,
            user=request.user,
            defaults={'score': score, 'review': review}
        )

        serializer = self.get_serializer(rating)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_subscribe(request: Request) -> Response:
    """
    POST /api/subscribe/
    Subscribe to the flan newsletter.
    """
    serializer = SubscribeSerializer(data=request.data)

    if serializer.is_valid():
        from .models import Subscriber
        subscriber, created = Subscriber.objects.get_or_create(
            email=serializer.validated_data['email'],
            defaults=serializer.validated_data
        )

        if created:
            return Response(
                {'message': f"Welcome to OnlyFlans, {subscriber.display_name}! 🍮"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': "You're already subscribed! We flan-tically appreciate you."},
                status=status.HTTP_200_OK
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_stats(request: Request) -> Response:
    """
    GET /api/stats/
    Platform-wide stats — great for a dashboard or README badges.
    """
    from .models import Subscriber
    stats = {
        'total_flans': Flan.objects.count(),
        'premium_flans': Flan.objects.filter(is_premium=True).count(),
        'free_flans': Flan.objects.filter(is_premium=False).count(),
        'total_creators': FlanCreator.objects.count(),
        'total_subscribers': Subscriber.objects.filter(is_active=True).count(),
        'total_ratings': FlanRating.objects.count(),
        'avg_platform_rating': round(
            FlanRating.objects.aggregate(avg=Avg('score'))['avg'] or 0, 1
        ),
        'flans_by_type': {
            flan_type: Flan.objects.filter(flan_type=flan_type).count()
            for flan_type, _ in Flan.FlanType.choices
        }
    }
    return Response(stats)
