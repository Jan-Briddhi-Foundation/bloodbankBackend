from django.urls import path
from .views import *

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='login_api'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout_api'),

    path('home/', HomePageAPIView.as_view(), name='home_api'),


    path('donor-home/', DonorHomeAPIView.as_view(), name='donor_home'),
    path('donation-criteria/', DonationCriteriaAPIView.as_view(),
         name='donation_criteria'),
    path('location-map/', LocationMapAPIView.as_view(), name='location_map'),
    path('not-eligible/', NotEligibleAPIView.as_view(), name='not_eligible'),
    path('thank-you/', ThankYouAPIView.as_view(), name='thank_you'),


    path('patient-home/', PatientHomeAPIView.as_view(), name='patient_home'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('edit-profile/', EditProfileAPIView.as_view(), name='edit_profile'),
    path('request-blood/', RequestBloodAPIView.as_view(), name='request_blood'),
    path('request-sent/', RequestSentAPIView.as_view(), name='request_sent'),
    path('patient-history/', PatientHistoryAPIView.as_view(),
         name='patient_history'),

    path('delete-page/<int:pk>/',
         DeletePageAPIView.as_view(), name='delete_page'),
    path('notifications/', NotificationsAPIView.as_view(),
         name='notifications'),
    path('blood-match-success/', BloodMatchSuccessAPIView.as_view(),
         name='blood_match_success'),
    path('error404/', Error404APIView.as_view(), name='error404'),

]
