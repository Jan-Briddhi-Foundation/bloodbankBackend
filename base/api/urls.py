from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register_api'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
    path('home/', HomePageAPIView.as_view(), name='home_api'),
    path('logout/', LogoutAPIView.as_view(), name='logout_api'),
    path('user-details/', UserDetailsAPIView.as_view(), name='user_details_api'),


    path('donor-home/', DonorHomeAPIView.as_view(), name='donor_home_api'),
    path('donation-criteria/', DonationCriteriaAPIView.as_view(),
         name='donation_criteria_api'),
    path('location-map/', LocationMapAPIView.as_view(), name='location_map_api'),
    path('not-eligible/', NotEligibleAPIView.as_view(), name='not_eligible_api'),
    path('thank-you/', ThankYouAPIView.as_view(), name='thank_you_api'),


    path('patient-home/', PatientHomeAPIView.as_view(), name='patient_home_api'),
    path('profile/', ProfileAPIView.as_view(), name='profile_api'),
    path('edit-profile/', EditProfileAPIView.as_view(), name='edit_profile_api'),
    path('request-blood/', RequestBloodAPIView.as_view(), name='request_blood_api'),
    path('request-sent/', RequestSentAPIView.as_view(), name='request_sent_api'),
    path('patient-history/', PatientHistoryAPIView.as_view(),
         name='patient_history_api'),

    path('delete-page/<int:pk>/',
         DeletePageAPIView.as_view(), name='delete_page_api'),
    path('notifications/', NotificationsAPIView.as_view(),
         name='notifications_api'),
    path('blood-match-success/', BloodMatchSuccessAPIView.as_view(),
         name='blood_match_success_api'),
    path('error404/', Error404APIView.as_view(), name='error404_api'),

]
