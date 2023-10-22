from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True, max_length=254)
    phone = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class BloodGroup(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ACCOUNT = (
        ('donor', 'I am a donor'),
        ('patient', 'I need a donor'),
    )

    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    bloodgroup = models.ForeignKey(
        BloodGroup, on_delete=models.SET_NULL, null=True)
    langauge = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)

    profile_pic = models.ImageField(
        default="avatar.svg", null=True, blank=True)

    profile_type = models.CharField(max_length=255, null=True, choices=ACCOUNT)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.name
