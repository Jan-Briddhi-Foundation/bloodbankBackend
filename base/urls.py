from django.contrib import admin
from django.urls import path

from .views import home, loginPage, logoutPage, registrationPage, UserDetails, PatientHome, DonorHome

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('registration/', registrationPage, name='registration'),
    path('logout/', logoutPage, name='logout'),

    path('', PatientHome, name='patient_home'),
    path('donor_page/', DonorHome, name='donor_home'),

    path('Personal details/', UserDetails, name='user_details'),
]
