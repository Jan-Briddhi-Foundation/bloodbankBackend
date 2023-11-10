from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, serializers
from .serializers import *
from .models import Profile, Blood_Request, Donation_Form
# Create your views here.


from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def profile(request):
    try:
        profile = Profile.objects.all()
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Profile_Serializer(profile, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def blood_request(request):
    try:
        request_blood = Blood_Request.objects.all()
    except request_blood.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Blood_Request_Serializer(request_blood, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def donate(request):
    try:
        donate_blood = Donation_Form.objects.all()
    except donate_blood.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = Donation_Criteria_Serializer(donate_blood, many=True)
    return Response(serializer.data)


# ////////////////////////////////
# ////////////////////////////////
# ////////////////////////////////

# Registration
# //////////////////////////////////////////////////

@permission_classes([AllowAny])
class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(username=request.data.get('email'))
            Profile.objects.create(user=user)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Email or password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class HomePageAPIView(APIView):
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


@permission_classes([IsAuthenticated])
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class UserDetailsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            profile = request.user.profile
            profile.city = serializer.validated_data['city']
            profile.country = serializer.validated_data['country']
            profile.bloodgroup = serializer.validated_data['bloodgroup']
            profile.profile_type = serializer.validated_data['profile_type']
            profile.save()
            return Response({'message': 'User details updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////
# 2. DONORS PAGES
# //////////////////////////////////////////////////////////////////

@permission_classes([IsAuthenticated])
class DonorHomeAPIView(APIView):
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


@permission_classes([IsAuthenticated])
class DonationCriteriaAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonationCriteriaFormSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(profile=request.user.profile)

            if donation_comparison_form(serializer):
                return Response({'message': 'Thank you'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Not eligible'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class LocationMapAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render location_map.html'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class NotEligibleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render not_eligible.html'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ThankYouAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render thank_you.html'}, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////
@permission_classes([IsAuthenticated])
class PatientHomeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'page': 'home_patient_page'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = ProfileFormSerializer(instance=user)

        return Response({'profile': profile.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class EditProfileAPIView(APIView):
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


@permission_classes([IsAuthenticated])
class RequestBloodAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile
        form = RequestBloodFormSerializer(instance=user_profile)

        return Response({'user': user, 'user_profile': user_profile, 'form': form.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.profile

        serializer = RequestBloodFormSerializer(data=request.data)
        if serializer.is_valid():
            blood_request = Blood_Request.objects.create(
                profile=user_profile,
                quantity=serializer.validated_data['quantity'],
                date_needed=serializer.validated_data['date_needed']
            )
            return Response({'message': 'Blood request sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class RequestSentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render request_sent.html'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class PatientHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        history = Blood_Request.objects.filter(profile__user=user)
        serializer = BloodRequestSerializer(history, many=True)

        return Response({'history': serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class DeletePageAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        return Response({'item': item}, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        item = Blood_Request.objects.get(id=pk)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class NotificationsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render notifications.html'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class BloodMatchSuccessAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render blood_match_success.html'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class Error404APIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Render error404.html'}, status=status.HTTP_200_OK)
