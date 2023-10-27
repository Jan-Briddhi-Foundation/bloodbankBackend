from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import *
from .decorators import unauthenticated_user
from .forms import RequestBloodForm, Donation_CriteriaForm, CreateUserForm, ProfileForm

# Create your views here.

# //////////////////////////////////////////////////////////////////
# 1. REGISTRATION PAGES
# //////////////////////////////////////////////////////////////////


@unauthenticated_user
def loginPage(request):
    page = 'login'

    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        user = None

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except:
                messages.error(request, "User does not exist")

            user = authenticate(
                request, email=username_or_email, password=password)

        else:
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, "User does not exist")

            user = authenticate(
                request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, "Login successful")

            profile_type = request.user.profile.profile_type
            print(profile_type)

            if profile_type == 'donor':
                return redirect('donor_home')
            elif profile_type == 'patient':
                return redirect('home')
            else:
                return redirect('donor_home')
        else:
            messages.error(request, "Username or Password is incorrect")

    context = {"page": page}
    return render(request, 'base/login_registration.html', context)


@unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Profile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, "Successfully registered " + username)
            # login(request, user)
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/login_registration.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

# //////////////////////////////////////////////////////////////////
# 2. DONORS PAGES
# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def DonorHome(request):
    page = 'home_donor_page'

    blood_requests = Blood_Request.objects.all()

    context = {'page': page, "blood_requests": blood_requests}
    return render(request, 'base/donor_homePage.html', context)


def donation_comparison_form(user_form_data):
    userChoice = []
    needed_values = [False, False, False,
                     False, False, False, False, False, False, False, True, True, True, False]

    for field_value in ['rabis_hepatitis_past_1_year', 'tatoo_surgery_past_6_months', 'donated_blood_past_3_months', 'immunisation_past_1_month', 'anitibiotics_past_48_hrs', 'alcoholic_bevarage_past_24_hrs', 'asprin_dentalwork_past_72_hrs', 'cough_common_presently', 'pregnant_breastFeeding_presently', 'menstration_presently', 'health_check_1', 'health_check_2', 'age_betwn_18_60', 'body_weight_less_45']:
        choice = user_form_data.cleaned_data.get(field_value)
        userChoice.append(choice)

    for i in range(len(needed_values)):
        if needed_values[i] != userChoice[i]:
            return False
    return True


@login_required(login_url='login')
def donationCriteria(request):
    form = Donation_CriteriaForm()
    if request.method == 'POST':
        form = Donation_CriteriaForm(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.profile = request.user.profile
            instance.save()

            if donation_comparison_form(form):
                return redirect('thankyou')
            else:
                return redirect('not_eligible')

    context = {"form": form}
    return render(request, 'base/donation_form.html', context)


@login_required(login_url='login')
def locationMap(request):

    context = {}
    return render(request, 'base/location_map.html', context)


@login_required(login_url='login')
def notEligible(request):

    context = {}
    return render(request, 'base/not_eligible.html', context)


@login_required(login_url='login')
def thankYou(request):

    context = {}
    return render(request, 'base/thank_you.html', context)

# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def PatientHome(request):
    page = 'home_patient_page'

    context = {'page': page}
    return render(request, 'base/donor_PatientPage.html', context)


@login_required(login_url='login')
def profile(request):
    user_profile = request.user.profile
    profile = ProfileForm(instance=user_profile)

    context = {"profile": profile}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def editprofile(request):
    user_profile = request.user.profile
    form = ProfileForm(instance=user_profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid:
            profile_pic = form.cleaned_data.get('profile_pic')

            if profile_pic:
                if not profile_pic.name.lower().endswith('.png'):
                    raise ValidationError("Only PNG files are allowed.")

            form.save()
            messages.success(request, "Profile updated")
            return redirect('profile')
        else:
            error_message = "Please upload a PNG file."

    context = {"form": form}
    return render(request, 'base/edit_profile.html', context)


@login_required(login_url='login')
def requestBlood(request):
    user_profile = request.user.profile
    form = RequestBloodForm(instance=user_profile)

    if request.method == "POST":
        blood_request = Blood_Request.objects.create(
            profile=request.user.profile,
            quantity=request.POST.get('quantity'),
            date_needed=request.POST.get('date_needed')
        )
        return redirect('request_sent')

    context = {"user_profile": user_profile, "form": form}
    return render(request, 'base/request_blood.html', context)


@login_required(login_url='login')
def requestSent(request):
    context = {}
    return render(request, 'base/request_sent.html', context)


@login_required(login_url='login')
def patientHistory(request):
    user = request.user
    history = Blood_Request.objects.filter(profile__user=user)

    context = {"history": history}
    return render(request, 'base/patient_history.html', context)


def deletePage(request, pk):
    item = Blood_Request.objects.get(id=pk)

    if request.method == "POST":
        item.delete()
        return redirect('/')

    return render(request, 'base/delete.html', {"item": item})


@login_required(login_url='login')
def notifications(request):
    context = {}
    return render(request, 'base/notifications.html', context)


@login_required(login_url='login')
def bloodMatchSuccess(request):
    context = {}
    return render(request, 'base/blood_match_success.html', context)


@login_required(login_url='login')
def error404(request):
    context = {}
    return render(request, 'error404.html', context)
