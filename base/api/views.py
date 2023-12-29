import requests

from django.urls import reverse
from django.contrib.auth import authenticate
from django.utils.timesince import timesince
from django.contrib.sites.models import Site

from .serializers import *
from base.utils import create_knox_token
from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form


from knox.auth import AuthToken
from knox.views import LoginView, LogoutView
from knox.views import LoginView as KnoxLoginView

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter

# Create your views here.


class LoginAPIView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            return Response({
                "user": UserSerializer(user).data,
                "token": create_knox_token(user=user)[1]
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": "Invalid credentials"},  status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(LogoutView):
    permission_classes = [IsAuthenticated]


class HomePageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
            request.user.name = f"{request.user.first_name} {request.user.last_name}"
            request.user.save()
            return Response({'message': 'User details updated'}, status=status.HTTP_200_OK)

        profile_type = request.user.profile.profile_type

        if profile_type == 'donor':
            redirect_url = reverse('donor_home')

        elif profile_type == 'patient':
            redirect_url = reverse('patient_home')

        else:
            redirect_url = reverse('user_details')

        return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            profile = request.user.profile
            profile.city = serializer.validated_data['city']
            profile.country = serializer.validated_data['country']
            profile.bloodGroup = serializer.validated_data['bloodGroup']
            profile.profile_type = serializer.validated_data['profile_type']
            profile.save()

            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetUserPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            current_site = Site.objects.get_current()
            current_site = 'localhost:8000'

            payload = {
                'uid': kwargs.get('uid'),
                'token': kwargs.get('token'),
                'new_password': serializer.validated_data['new_password'],
                're_new_password': serializer.validated_data['re_new_password']
            }

            djoser_password_reset_url = 'api/auth/users/reset_password_confirm/'

            protocol = 'https'
            headers = {'content-Type': 'application/json'}

            if not request.is_secure():
                protocol = 'http'

            url = f'{protocol}://{current_site}/{djoser_password_reset_url}'

            try:
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 204:
                    return Response({'message': 'Password Successfully updated'}, status=status.HTTP_200_OK)
                else:
                    response_object = response.json()

                    return Response({'errors': response_object}, status=response.status_code)

            except requests.RequestException as e:
                return Response({'errors': 'Error in making request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////
# SOCIAL AUTH
# //////////////////////////////////////////////////////////////////

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000//api/auth/google/login/'
    client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


# //////////////////////////////////////////////////////////////////
# 2. DONORS PAGES
# //////////////////////////////////////////////////////////////////


class DonorHomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blood_requests = Blood_Request.objects.all()
        serializer = BloodRequestSerializer(blood_requests, many=True)
        return Response({'blood_requests': serializer.data}, status=status.HTTP_200_OK)


def donation_comparison_form(user_form_data):
    user_choice = user_form_data.validated_data['qualify']
    return user_choice == True


class DonationCriteriaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.profile.profile_type != 'donor':
            return Response({'message': 'Only a donor can fill the form'}, status=status.HTTP_200_OK)

        serializer = DonationCriteriaFormSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save(profile=request.user.profile)

            if donation_comparison_form(serializer):
                message = 'Eligible to donate Blood'
                redirect_url = reverse('donation_agreement')
            else:
                message = 'Not Eligible to donate Blood'

            return Response({'redirect_url': redirect_url, 'message': message}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        userForm = EditUserFormSerializer(instance=user)
        profileForm = ProfileFormSerializer(instance=user_profile)

        return Response({'userForm': userForm.data, 'profileForm': profileForm.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        userForm = EditUserFormSerializer(
            data=request.data, instance=user)
        profileForm = ProfileFormSerializer(
            data=request.data, instance=user_profile)

        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response({'erros': 'Please upload a PNG file.'}, status=status.HTTP_400_BAD_REQUEST)


class RequestBloodAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        if user.profile.profile_type != 'patient':
            return Response({'message': 'Only a patient can request blood.'}, status=status.HTTP_200_OK)

        serializer = BloodRequestSerializer(
            data=request.data, instance=user_profile)
        if serializer.is_valid():
            blood_request = Blood_Request.objects.create(
                profile=user_profile,
                quantity=serializer.validated_data['quantity'],
                date_needed=serializer.validated_data['date_needed']
            )
            return Response({'message': 'Blood request success'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user.profile
        history = Blood_Request.objects.filter(profile__user=user)
        profileForm = ProfileFormSerializer(instance=user_profile)
        serializer = BloodRequestSerializer(history, many=True)

        return Response({'history': serializer.data, 'profileForm': profileForm.data}, status=status.HTTP_200_OK)


class HospitalAddresses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hospital_address = HospitalAddress.objects.all()
        hospitals = HospitalAddressSerializer(hospital_address, many=True)
        return Response({'hospitals': hospitals.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = HospitalAddressSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({'message': 'Hopsital added successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationAgreement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user.profile
        donations = Donation.objects.filter(profile__user=user)
        serializer = DonationAgreementSerializer(donations, many=True)
        profileForm = ProfileFormSerializer(instance=user_profile)

        return Response({'history': serializer.data, 'profileForm': profileForm.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        serializer = DonationAgreementSerializer(
            data=request.data, instance=user_profile)

        if serializer.is_valid():
            donationAgreement = Donation.objects.create(
                profile=user_profile,
                hospital_address=serializer.validated_data['hospital_address'],

            )
            return Response({'message': 'Successfully sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonationCriteriaQuestionsSerializer

    def get(self, request, *args, **kwargs):
        criteria_quiz = DonationCriteriaQuestions.objects.all()
        questions = self.serializer_class(criteria_quiz, many=True)
        return Response({'questions': questions.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        if not user.is_staff:
            return Response({'errors': 'Only admin users can create questions.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            donationQuestion = DonationCriteriaQuestions.objects.create(
                profile=user_profile,
                question=serializer.validated_data['question'],
            )
            return Response({'message': 'Successfully sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return Response({'errors': 'Only admin users can update questions.'}, status=status.HTTP_403_FORBIDDEN)

        question_id = kwargs.get('question_id')
        try:
            question = DonationCriteriaQuestions.objects.get(id=question_id)
        except DonationCriteriaQuestions.DoesNotExist:
            return Response({'errors': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DonationCriteriaQuestionsSerializer(
            question, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Question updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return Response({'errors': 'Only admin users can delete questions.'}, status=status.HTTP_403_FORBIDDEN)

        question_id = kwargs.get('question_id')
        try:
            question = DonationCriteriaQuestions.objects.get(id=question_id)
        except DonationCriteriaQuestions.DoesNotExist:
            return Response({'errors': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response({'message': 'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class NotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        user = request.user
        profile = user.profile
        profile_type = profile.profile_type

        if profile_type == 'patient':
            requests = Donation_Criteria_Form.objects.all()

            filtered_requests = [
                request for request in requests if request.profile.bloodGroup == profile.bloodGroup and request.qualify]

            bloodRequests = DonationCriteriaFormSerializer(
                filtered_requests, many=True)

        else:
            requests = Blood_Request.objects.all()

            filtered_requests = [
                request for request in requests if request.profile.city == profile.city]

            bloodRequests = BloodRequestSerializer(
                filtered_requests, many=True)

        return Response({'requests': bloodRequests.data}, status=status.HTTP_200_OK)
