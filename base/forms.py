from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import User, Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'country', 'bloodgroup', 'profile_type']
        # exclude = ['user', 'profile_type']
