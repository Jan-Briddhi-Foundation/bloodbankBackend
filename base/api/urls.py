from django.urls import path
from .views import *

from knox import views as knox_views
# from yourapp.api.views import LoginView

urlpatterns = [
    #     path('auth/login/', LoginAPIView.as_view(), name='login_api'),
    #     path('auth/logout/', LogoutAPIView.as_view(), name='logout_api'),
    #     path('auth/validate/', userValidateAPI, name='user_validate'),

    path('auth/login/', LoginAPIView.as_view(), name='knox_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(),
         name='knox_logoutall'),


    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),


    path('home/', HomePageAPIView.as_view(), name='home'),

    path('personal-details/', UserDetailsAPIView.as_view(), name='user_details'),


    path('donor-home/', DonorHomeAPIView.as_view(), name='donor_home'),
    path('donation-criteria/', DonationCriteriaAPIView.as_view(),
         name='donation_criteria'),
    path('location-map/', LocationMapAPIView.as_view(), name='location_map'),
    path('not-eligible/', NotEligibleAPIView.as_view(), name='not_eligible'),


    path('donation-agreement/', DonationAgreement.as_view(),
         name='donation_agreement'),
    path('hospital-address/', HospitalAddress.as_view(), name='hospital_address'),


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
