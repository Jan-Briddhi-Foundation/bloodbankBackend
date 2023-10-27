from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodgroup', 'profile_type']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']


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
