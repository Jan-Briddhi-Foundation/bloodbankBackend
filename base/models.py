from django.contrib.auth.models import AbstractUser
from django.db import models

# Adrenaline junky


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


class Blood_Request(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_needed = models.DateField(auto_now_add=False, null=True)

    def __str__(self):
        return self.profile.user.name


class Donation_Form(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    rabis_hepatitis_past_1_year = models.BooleanField(null=True)
    tatoo_surgery_past_6_months = models.BooleanField(null=True)
    donated_blood_past_3_months = models.BooleanField(null=True)
    immunisation_past_1_month = models.BooleanField(null=True)
    anitibiotics_past_48_hrs = models.BooleanField(null=True)
    alcoholic_bevarage_past_24_hrs = models.BooleanField(null=True)
    asprin_dentalwork_past_72_hrs = models.BooleanField(null=True)
    cough_common_presently = models.BooleanField(null=True)
    pregnant_breastFeeding_presently = models.BooleanField(null=True)
    menstration_presently = models.BooleanField(null=True)
    health_check_1 = models.BooleanField(null=True)
    health_check_2 = models.BooleanField(null=True)
    age_betwn_18_60 = models.BooleanField(null=True)
    body_weight_less_45 = models.BooleanField(null=True)

    def __str__(self):
        return self.profile.user.name
