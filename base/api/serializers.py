from rest_framework import serializers
from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Form


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


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Form
        fields = '__all__'


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Request
        fields = '__all__'
