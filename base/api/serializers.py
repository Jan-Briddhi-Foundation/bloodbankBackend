from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Criteria_Form, DonationCriteriaQuestions, HospitalAddress, Donation

from rest_framework import serializers


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


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodGroup', 'profile_type']


class BloodRequestSerializer(serializers.ModelSerializer):
    quantity = serializers.FloatField()
    date_needed = serializers.DateField()
    profile = ProfileSerializer()

    class Meta:
        model = Blood_Request
        fields = '__all__'


class BloodRequestSerializerpro(serializers.ModelSerializer):
    quantity = serializers.FloatField()
    date_needed = serializers.DateField()

    class Meta:
        model = Blood_Request
        fields = '__all__'


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    qualify = serializers.BooleanField()

    class Meta:
        model = Donation_Criteria_Form
        fields = '__all__'


class EditUserFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']


class ProfileFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user', 'date_created', 'date_modified']


class HospitalAddressSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = HospitalAddress
        fields = ['id', 'name', 'address', 'email']


class DonationCriteriaQuestionsSerializer(serializers.ModelSerializer):
    question = serializers.CharField()

    class Meta:
        model = DonationCriteriaQuestions
        fields = ['id', 'question']


class DonationAgreementSerializer(serializers.ModelSerializer):
    hospital_address = HospitalAddress()

    class Meta:
        model = Donation
        fields = '__all__'


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()
