from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.profile, name='profile'),
    path('requests/', views.blood_request, name='blood_requests'),
    path('donate/', views.donate, name='donation')
]
