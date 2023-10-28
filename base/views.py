from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import *
from .decorators import *
from .forms import CreateUserForm, UserDetailsForm, EditUserForm, RequestBloodForm, Donation_CriteriaForm, ProfileForm
# Create your views here.


@unauthenticated_user
def registrationPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.username = form.cleaned_data.get('email')
            instance.save()

            user = form.instance
            Profile.objects.create(user=user)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return redirect('user_details')

    context = {"form": form}
    return render(request, 'base/login_registration_page.html', context)


@unauthenticated_user
def loginPage(request):
    page = 'login'

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, "Login successful")
            return redirect('home')

        else:
            messages.error(request, "Email or Password is incorrect")

    context = {"page": page}
    return render(request, 'base/login_registration_page.html', context)


@login_required(login_url='login')
def homePage(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=request.user)
        request.user.name = f"{request.user.first_name} {request.user.last_name}"
        request.user.save()
        return redirect('user_details')

    profile_type = request.user.profile.profile_type

    if profile_type == 'donor':
        return redirect('donor_home')
    elif profile_type == 'patient':
        return redirect('patient_home')
    else:
        return redirect('user_details')


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def UserDetails(request):
    form = UserDetailsForm()

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)

        if form.is_valid():
            profile = request.user.profile

            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            profile.bloodgroup = form.cleaned_data['bloodgroup']
            profile.profile_type = form.cleaned_data['profile_type']

            profile.save()

            return redirect('home')

    context = {"form": form}

    return render(request, 'base/userDetails_page.html', context)


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
    return render(request, 'base/location_map.html', {})


@login_required(login_url='login')
def notEligible(request):
    return render(request, 'base/not_eligible.html')


@login_required(login_url='login')
def thankYou(request):
    return render(request, 'base/thank_you.html')


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
    user = request.user
    profile = ProfileForm(instance=user)

    context = {"profile": profile}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def editprofile(request):
    user = request.user
    user_profile = user.profile

    userForm = EditUserForm(instance=user)
    profileForm = ProfileForm(instance=user_profile)

    if request.method == 'POST':
        userForm = EditUserForm(request.POST, instance=user)
        profileForm = ProfileForm(
            request.POST, request.FILES, instance=user_profile)
        # form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        # if form.is_valid:
        #     profile_pic = form.cleaned_data.get('profile_pic')

        #     if profile_pic:
        #         if not profile_pic.name.lower().endswith('.png'):
        #             raise ValidationError("Only PNG files are allowed.")

        #     form.save()
        #     messages.success(request, "Profile updated")
        #     return redirect('profile')
        # else:
        #     error_message = "Please upload a PNG file."
        if userForm.is_valid and profileForm.is_valid:
            userForm.save()
            profileForm.save()
            messages.success(request, "Profile updated")
            return redirect('profile')
        else:
            error_message = "Please upload a PNG file."

    context = {"userForm": userForm, "profileForm": profileForm}
    return render(request, 'base/edit_profile.html', context)


@login_required(login_url='login')
def requestBlood(request):
    user = request.user
    user_profile = user.profile
    form = RequestBloodForm(instance=user_profile)

    if request.method == "POST":
        blood_request = Blood_Request.objects.create(
            profile=request.user.profile,
            quantity=request.POST.get('quantity'),
            date_needed=request.POST.get('date_needed')
        )
        return redirect('request_sent')

    context = {"user": user, "user_profile": user_profile, "form": form}
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


@login_required(login_url='login')
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
