from django.urls import path
from . import views

urlpatterns = [
    # Flan list & detail
    path('', views.flan_list, name='flan-list'),
    path('flan/<int:flan_id>/', views.flan_detail, name='flan-detail'),
    path('flan/<int:flan_id>/rate/', views.rate_flan, name='flan-rate'),  # NEW
    path('flan/create/', views.create_flan,
         name='flan-create'),           # FIX: was missing

    # Static pages
    path('faq/', views.faq, name='faq'),

    # Subscriptions
    path('subscribe/', views.subscribe, name='subscribe'),

    # Creators
    path('creators/', views.creators_list, name='creators-list'),
    path('creator/<int:creator_id>/', views.creator_detail, name='creator-detail'),
]
