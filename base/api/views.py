from rest_framework.response import Response
from .serializers import *
from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form
from django.contrib.auth import authenticate
from knox.auth import AuthToken
from knox.views import LoginView, LogoutView

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.utils import create_knox_token
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
            return Response({'redirect': 'donor_home'}, status=status.HTTP_302_FOUND)
        elif profile_type == 'patient':
            return Response({'redirect': 'patient_home'}, status=status.HTTP_302_FOUND)
        else:
            return Response({'redirect': 'user_details'}, status=status.HTTP_302_FOUND)


class LogoutAPIView(LogoutView):
    permission_classes = [IsAuthenticated]

# //////////////////////////////////////////////////////////////////
# 2. DONORS PAGES
# //////////////////////////////////////////////////////////////////


class DonorHomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        blood_requests = Blood_Request.objects.all()
        serializer = BloodRequestSerializer(blood_requests, many=True)
        return Response({'page': 'home_donor_page', 'blood_requests': serializer.data}, status=status.HTTP_200_OK)


def donation_comparison_form(user_form_data):
    userChoice = []
    needed_values = [False, False, False,
                     False, False, False, False, False, False, False, True, True, True, False]

    for field_value in ['rabis_hepatitis_past_1_year', 'tatoo_surgery_past_6_months', 'donated_blood_past_3_months', 'immunisation_past_1_month', 'anitibiotics_past_48_hrs', 'alcoholic_bevarage_past_24_hrs', 'asprin_dentalwork_past_72_hrs', 'cough_common_presently', 'pregnant_breastFeeding_presently', 'menstration_presently', 'health_check_1', 'health_check_2', 'age_betwn_18_60', 'body_weight_less_45']:
        choice = user_form_data.cleaned_data.get(field_value)
        userChoice.append(choice)

    for i in range(len(needed_values)):
        if needed_values[i] != userChoice[i]:
            return False
    return True


class DonationCriteriaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DonationCriteriaFormSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(profile=request.user.profile)

            if donation_comparison_form(serializer):
                return Response({'message': 'Thank you'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Not eligible'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationMapAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render location_map.html'}, status=status.HTTP_200_OK)


class NotEligibleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render not_eligible.html'}, status=status.HTTP_200_OK)


class ThankYouAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render thank_you.html'}, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////

class PatientHomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'page': 'home_patient_page'}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = request.user.profile
        profile = ProfileFormSerializer(instance=user_profile)

        return Response({'profile': profile.data}, status=status.HTTP_200_OK)


class EditProfileAPIView(APIView):
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

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile
        form = BloodRequestSerializer(instance=user_profile)

        return Response({'user': user, 'user_profile': user_profile, 'form': form.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        serializer = BloodRequestSerializer(data=request.data)
        if serializer.is_valid():
            blood_request = Blood_Request.objects.create(
                profile=user_profile,
                quantity=serializer.validated_data['quantity'],
                date_needed=serializer.validated_data['date_needed']
            )
            return Response({'message': 'Blood request sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestSentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render request_sent.html'}, status=status.HTTP_200_OK)


class PatientHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        history = Blood_Request.objects.filter(profile__user=user)
        serializer = BloodRequestSerializer(history, many=True)

        return Response({'history': serializer.data}, status=status.HTTP_200_OK)


class DeletePageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        return Response({'item': item}, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)


class NotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render notifications.html'}, status=status.HTTP_200_OK)


class BloodMatchSuccessAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render blood_match_success.html'}, status=status.HTTP_200_OK)


class Error404APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render error404.html'}, status=status.HTTP_200_OK)
