from django.urls import path
from .views import *

from knox import views as knox_views

urlpatterns = [

    path('auth/login/', LoginAPIView.as_view(), name='knox_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(),
         name='knox_logoutall'),

    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),


    path('home/', HomePageAPIView.as_view(), name='home'),   # 7

    path('profile-details/', UserDetailsAPIView.as_view(),
         name='user_details'),   # 6


    path('donor-home/', DonorHomeAPIView.as_view(), name='donor_home'),   # 5
    path('donation-criteria/', DonationCriteriaAPIView.as_view(),
         name='donation_criteria'),   # 8
    path('questions/', QuestionsAPIView.as_view(),
         name='criteria_quizes'),
    path('questions/<int:question_id>/', QuestionsAPIView.as_view(),
         name='criteria_quizes'),
    #     path('not-eligible/', NotEligibleAPIView.as_view(), name='not_eligible'),


    path('donation-agreement/', DonationAgreement.as_view(),
         name='donation_agreement'),   # 4
    path('hospital-address/', HospitalAddress.as_view(),
         name='hospital_address'),  # 9


    #     path('patient-home/', PatientHomeAPIView.as_view(), name='patient_home'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),  # 3
    #     #     path('profile-edit/', EditProfileAPIView.as_view(), name='edit_profile'),
    path('request-blood/', RequestBloodAPIView.as_view(),
         name='request_blood'),  # 2
    #     path('request-sent/', RequestSentAPIView.as_view(), name='request_sent'),
    path('patient-history/', PatientHistoryAPIView.as_view(),
         name='patient_history'),  # 1

    #     path('delete-page/<int:pk>/',
    #          DeletePageAPIView.as_view(), name='delete_page'),
    path('notifications/', NotificationsAPIView.as_view(),
         name='notifications'),
    #     path('blood-match-success/', BloodMatchSuccessAPIView.as_view(),
    #          name='blood_match_success'),
    #     path('error404/', Error404APIView.as_view(), name='error404'),

]
