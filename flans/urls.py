from django.urls import path
from . import views

urlpatterns = [
    path('', views.flan_list, name='flan-list'),
    path('flan/<int:flan_id>/', views.flan_detail,
         name='flan-detail'),
    path('faq/', views.faq, name='faq'),

]
# Interview Concept: URL patterns with parameters (<int:flan_id>) capture values from the URL and pass them to views.
