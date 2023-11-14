from rest_framework import serializers
from ..models import User, BloodGroup, Profile, Blood_Request, Donation_Form


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Profile
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = [ "name", "email", "password", "profile"]
    def create(self, validated_data):
        profile_data = validated_data.get("profile")
        if profile_data:
            validated_data.pop("profile")
        user = User.objects.create_user( **validated_data)
        
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)
        
    
        if profile_data and isinstance(profile_data, dict) :
            for key, value in profile_data.items():
                profile.country = profile.__setattr__( key, value)
            profile.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()

class UserDetailsSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    bloodgroup = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["name",'email']
    
    def get_city(self, obj):
        return obj.profile.city
        
    def get_full_name (self, obj):
        return f"{obj.last_name} {obj.first_name}"
    def get_country (self, obj):
        return obj.profile.country
    def get_bloodgroup (self, obj):
        return obj.profile.bloodgroup
    def get_profile_type (self, obj):
        return obj.profile.profile_type


class DonationCriteriaFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Form
        fields = '__all__'


class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Request
        fields = '__all__'
