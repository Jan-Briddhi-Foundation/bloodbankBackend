from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import User, Profile, Blood_Request, Donation_Form


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodgroup', 'profile_type']


# from django.contrib.auth.forms import UserCreationForm
# # from django.contrib.auth.models import User

# from django import forms
# from .models import *


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('name', 'phone', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'profile_type']


class RequestBloodForm(forms.ModelForm):
    class Meta:
        model = Blood_Request
        fields = '__all__'
        exclude = ['profile']


class Donation_CriteriaForm(forms.ModelForm):
    class Meta:
        model = Donation_Form
        fields = '__all__'
        exclude = ['profile']
