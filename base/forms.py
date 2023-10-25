from allauth.account.forms import SignupForm
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


class CustomSignupForm(SignupForm):
    role = forms.ChoiceField(
        choices=(('patient', 'Patient'), ('donor', 'Donor')),
        widget=forms.RadioSelect,
        label='I am a:'
    )
