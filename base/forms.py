from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email']
