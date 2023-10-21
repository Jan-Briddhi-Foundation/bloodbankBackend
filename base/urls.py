from django.contrib import admin
from django.urls import path

from .views import home, loginPage, registrationPage

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('registration/', registrationPage, name='registration'),

]
