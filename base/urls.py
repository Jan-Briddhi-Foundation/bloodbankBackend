from django.contrib import admin
from django.urls import path

from .views import home, loginPage, registrationPage, UserDetails

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('registration/', registrationPage, name='registration'),
    path('logout/', logoutPage, name='logout'),

    path('Personal details/', UserDetails, name='user_details'),


]
