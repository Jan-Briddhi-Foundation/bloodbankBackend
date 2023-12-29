from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager

from typing import Any


class UserManager(UserManager):
    def create_user(self, name: str, email: str, password: str, **extra_fields: Any) -> Any:
        if not email:
            raise ValueError("Email Is required")
        email = self.normalize_email(email=email)
        user = self.model(name=name, email=email,  **extra_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, name: str, email: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields.get("is_staff") == True:
            raise ValueError("is_staff must be True")
        if not extra_fields.get("is_superuser") == True:
            raise ValueError("is_superuser must be True")
        return self.create_user(name=name, email=email, password=password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=200, unique=False, blank=True, null=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True, max_length=254)
    phone = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return self.email


class BloodGroup(models.TextChoices):
    A_POSITIVE = 'A+', 'A+'
    A_NEGATIVE = 'A-', 'A-'
    B_POSITIVE = 'B+', 'B+'
    B_NEGATIVE = 'B-', 'B-'
    AB_POSITIVE = 'AB+', 'AB+'
    AB_NEGATIVE = 'AB-', 'AB-'
    O_POSITIVE = 'O+', 'O+'
    O_NEGATIVE = 'O-', 'O-'


class Profile(models.Model):
    ACCOUNT = (
        ('donor', 'I am a donor'),
        ('patient', 'I need a donor'),
        ('none', 'none'),
    )

    user = models.OneToOneField(
        User, blank=True, on_delete=models.CASCADE, unique=True, related_name="profile")
    bloodGroup = models.CharField(max_length=3, choices=BloodGroup.choices)
    langauge = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)

    profile_pic = models.ImageField(
        default="avatar.svg", null=True, blank=True)

    profile_type = models.CharField(
        max_length=255, null=True, default="none", choices=ACCOUNT)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.name


class Blood_Request(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_needed = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return self.profile.user.name


class Donation_Criteria_Form(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    qualify = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.profile.user.name


class DonationCriteriaQuestions(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    question = models.CharField(max_length=355)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.question


class HospitalAddress(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    country = models.CharField(null=True, blank=True, max_length=150)
    states = models.CharField(null=True, blank=True, max_length=150)
    contact = models.CharField(null=True, blank=True, max_length=50)
    website = models.URLField(null=True, blank=True, max_length=200)
    email = models.EmailField(null=True, blank=True, max_length=254)
    location_longitude = models.CharField(
        null=True, blank=True, max_length=254)
    location_latitude = models.CharField(null=True, blank=True, max_length=254)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Donation(models.Model):
    profile = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)

    hospital_address = models.ForeignKey(
        HospitalAddress, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.profile.user.name


# Check if a profile already exists for the user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)
