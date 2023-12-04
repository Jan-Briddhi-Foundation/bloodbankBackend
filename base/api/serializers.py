from rest_framework import serializers
from ..models import (User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form, Donation,
                      DonorCriteriaFormSubmission, HospitalAddress, DonationCriteriaFormField, DonorCriteriaFormFieldData)


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
    class Meta:
        model = Blood_Request
        fields = '__all__'
        exclude = ['profile']


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Criteria_Form
        fields = '__all__'
        exclude = ['profile']


class DonationAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['hospital_address', 'eligibilityForm']


class EditUserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']


class ProfileFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'profile_type']


class HospitalAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = HospitalAddress
        fields = '__all__'


class DonationCriteriaFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCriteriaFormField
        fields = '__all__'


class DonorCriteriaFormFieldDataSerializer(serializers.ModelSerializer):
    field = DonationCriteriaFormFieldSerializer()

    class Meta:
        model = DonorCriteriaFormFieldData
        fields = '__all__'


class DonorCriteriaFormSubmissionSerializer(serializers.ModelSerializer):
    fields = DonorCriteriaFormFieldDataSerializer(many=True)

    class Meta:
        model = DonorCriteriaFormSubmission
        fields = '__all__'


class DonationsSerializer(serializers.ModelSerializer):
    hospital_address = HospitalAddress()
    eligibilityForm = DonorCriteriaFormSubmissionSerializer()

    class Meta:
        model = Donation
        fields = '__all__'


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()
