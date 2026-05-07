from django.urls import path
from . import api_views

urlpatterns = [
    # Flans
    path('flans/', api_views.FlanListAPIView.as_view(), name='api-flan-list'),
    path('flans/<int:pk>/', api_views.FlanDetailAPIView.as_view(), name='api-flan-detail'),
    path('flans/<int:flan_id>/ratings/', api_views.FlanRatingListCreateAPIView.as_view(), name='api-flan-ratings'),

    # Creators
    path('creators/', api_views.FlanCreatorListAPIView.as_view(), name='api-creators-list'),

    # Subscriptions
    path('subscribe/', api_views.api_subscribe, name='api-subscribe'),

    # Stats
    path('stats/', api_views.api_stats, name='api-stats'),
]