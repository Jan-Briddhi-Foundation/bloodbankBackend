
from django.utils.timesince import timesince
from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form
from django.contrib.auth import authenticate
from django.urls import reverse

from .serializers import *
from knox.auth import AuthToken
from knox.views import LoginView, LogoutView

from rest_framework.authentication import BasicAuthentication
from knox.views import LoginView as KnoxLoginView

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.utils import create_knox_token


from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from ..forms import CreateUserForm
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
            return Response({"error": "Invalid credentials"},  status=status.HTTP_400_BAD_REQUEST)


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


# def donation_comparison_form(user_form_data):
#     userChoice = []
#     needed_values = [False, False, False,
#                      False, False, False, False, False, False, False, True, True, True, False]

#     for field_value in ['rabis_hepatitis_past_1_year', 'tatoo_surgery_past_6_months', 'donated_blood_past_3_months', 'immunisation_past_1_month', 'anitibiotics_past_48_hrs', 'alcoholic_bevarage_past_24_hrs', 'asprin_dentalwork_past_72_hrs', 'cough_common_presently', 'pregnant_breastFeeding_presently', 'menstration_presently', 'health_check_1', 'health_check_2', 'age_betwn_18_60', 'body_weight_less_45']:
#         choice = user_form_data.cleaned_data.get(field_value)
#         userChoice.append(choice)

#     for i in range(len(needed_values)):
#         if needed_values[i] != userChoice[i]:
#             return False
#     return True

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


class LocationMapAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Location_map render'}, status=status.HTTP_200_OK)


class NotEligibleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Not Eligible'}, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////

class PatientHomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Patient Home page'}, status=status.HTTP_200_OK)


# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user_profile = request.user.profile
#         profile = ProfileFormSerializer(instance=user_profile)

#         return Response({'profile': profile.data}, status=status.HTTP_200_OK)


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
        return Response({'error_message': 'Please upload a PNG file.'}, status=status.HTTP_400_BAD_REQUEST)


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


class RequestSentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Request Sent Successfully'}, status=status.HTTP_200_OK)


class PatientHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = request.user.profile
        history = Blood_Request.objects.filter(profile__user=user)
        profileForm = ProfileFormSerializer(instance=user_profile)
        serializer = BloodRequestSerializer(history, many=True)

        return Response({'history': serializer.data, 'profileForm': profileForm.data}, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     user_profile = user.profile

    #     userForm = EditUserFormSerializer(instance=user)
    #     profileForm = ProfileFormSerializer(instance=user_profile)

    #     return Response({'userForm': userForm.data, 'profileForm': profileForm.data}, status=status.HTTP_200_OK)


class DeletePageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        return Response({'item': item}, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        item.delete()
        return Response({'message': 'Deleted successfully'}, status=status.HTTP_200_OK)


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


class HospitalAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = HospitalAddressSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({'message': 'Hopsital added successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonationCriteriaQuestionsSerializer

    def get(self, request, *args, **kwargs):
        criteria_quiz = DonationCriteriaQuestions.objects.all()
        questions = self.serializer_class(
            criteria_quiz, many=True)
        return Response({'questions': questions.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            donationQuestion = DonationCriteriaQuestions.objects.create(
                profile=user_profile,
                question=serializer.validated_data['question'],
            )
            return Response({'message': 'Successfully sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        try:
            question = DonationCriteriaQuestions.objects.get(id=question_id)
        except DonationCriteriaQuestions.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DonationCriteriaQuestionsSerializer(
            question, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Question updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        try:
            question = DonationCriteriaQuestions.objects.get(id=question_id)
        except DonationCriteriaQuestions.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

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


class BloodMatchSuccessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render blood_match_success.html'}, status=status.HTTP_200_OK)


class Error404APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render error404.html'}, status=status.HTTP_200_OK)


# @api_view(["POST"])
# def userValidateAPI(request):

#     userForm = CreateUserForm(**request.data)
#     if userForm.is_valid():
#         return Response({"message": "Form Valid"}, status=status.HTTP_200_OK)

#     return Response(userForm.error_messages, status=status.HTTP_401_UNAUTHORIZED)
