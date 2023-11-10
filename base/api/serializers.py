from rest_framework import serializers
from .models import User, BloodGroup, Profile, Blood_Request, Donation_Form


# class Profile_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'


# class Blood_Request_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blood_Request
#         fields = '__all__'


# class Donation_Criteria_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Donation_Form
#         fields = '__all__'


# //////////////////////////////////////////////////


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodgroup', 'profile_type']


class DonationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Criteria
        fields = '__all__'


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_CriteriaForm
        fields = '__all__'


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Request
        fields = '__all__'
