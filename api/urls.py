from django.urls import path
from . import views

urlpatterns = [
    path('api/profiles', views.profile, name='profile'),
    path('api/requests', views.blood_request, name='blood_requests'),
    path('api/donate', views.donate, name='donation')
]