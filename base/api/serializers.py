from rest_framework import serializers
# from ..models import (User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form, Donation,
#                       DonorCriteriaFormSubmission, HospitalAddress, DonationCriteriaFormField, DonorCriteriaFormFieldData)
from ..models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ["name", "email", "phone", "password", "profile"]

    def create(self, validated_data):
        profile_data = validated_data.get("profile")
        if profile_data:
            validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)

        if profile_data and isinstance(profile_data, dict):
            for key, value in profile_data.items():
                profile.country = profile.__setattr__(key, value)
            profile.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodGroup', 'profile_type']


class BloodRequestSerializer(serializers.ModelSerializer):
    quantity = serializers.FloatField()
    date_needed = serializers.DateField()

    class Meta:
        model = Blood_Request
        fields = '__all__'
        # exclude = ['profile']


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    qualify = serializers.BooleanField()

    class Meta:
        model = Donation_Criteria_Form
        fields = '__all__'
        # exclude = ['profile']


class EditUserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']


class ProfileFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user', 'profile_type',
                   'date_created', 'date_modified']


class HospitalAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = HospitalAddress
        fields = '__all__'


class DonationCriteriaQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.CharField()

    class Meta:
        model = DonationCriteriaQuestions
        fields = ['id', 'question']


# class DonorCriteriaFormFieldDataSerializer(serializers.ModelSerializer):
#     field = DonationCriteriaFormFieldSerializer()

#     class Meta:
#         model = DonorCriteriaFormFieldData
#         fields = '__all__'


# class DonorCriteriaFormSubmissionSerializer(serializers.ModelSerializer):
#     fields = DonorCriteriaFormFieldDataSerializer(many=True)

#     class Meta:
#         model = DonorCriteriaFormSubmission
#         fields = '__all__'


class DonationsSerializer(serializers.ModelSerializer):
    hospital_address = HospitalAddress()
    # eligibilityForm = DonorCriteriaFormSubmissionSerializer()

    class Meta:
        model = Donation
        fields = '__all__'


class DonationAgreementSerializer(serializers.ModelSerializer):
    hospital_address = HospitalAddressSerializer()

    class Meta:
        model = Donation
        fields = '__all__'


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()
