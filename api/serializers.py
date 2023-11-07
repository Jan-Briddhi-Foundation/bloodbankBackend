from rest_framework import serializers
from .models import *

class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class Blood_Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_Request
        fields = '__all__'

class Donation_Criteria_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Form
        fields = '__all__'
