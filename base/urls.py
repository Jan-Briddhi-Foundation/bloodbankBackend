from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('registration/', registrationPage, name='registration'),
    path('logout/', logoutPage, name='logout'),

    path('Personal details/', UserDetails, name='user_details'),

    path('', homePage, name='home'),
    path('patient_home', PatientHome, name='patient_home'),
    path('donor_home', DonorHome, name='donor_home'),

    path('donation_form/', donationCriteria, name='donation_form'),
    path('thankyou/', thankYou, name='thankyou'),
    path('not_eligible/', notEligible, name='not_eligible'),
    path('location_map/', locationMap, name='location_map'),

    path('delete/<str:pk>/', deletePage, name='delete_request'),

    path('profile/', profile, name='profile'),
    path('Edit Profile/', editprofile, name='editprofile'),

    path('Request Blood/', requestBlood, name='request_blood'),
    path('Request Sent/', requestSent, name='request_sent'),
    path('Patient History/', patientHistory, name='patient_history'),

    path('Notifications/', notifications, name='notifications'),
    path('Blood Match Success/', bloodMatchSuccess, name='blood_match_success'),
    path('ERROR/', error404, name='error404'),
]
