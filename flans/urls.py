from django.urls import path
from . import views

urlpatterns = [
    path('', views.flan_list, name='flan-list'),
    path('flan/<int:flan_id>/', views.flan_detail,
         name='flan-detail'),
    path('faq/', views.faq, name='faq'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('creators/', views.creators_list, name='creators-list'),  
    path('creator/<int:creator_id>/', views.creator_detail, name='creator-detail'), 

]
# Interview Concept: URL patterns with parameters (<int:flan_id>) capture values from the URL and pass them to views.
