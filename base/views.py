from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import Profile, User
from .forms import CreateUserForm, UserDetailsForm
# Create your views here.


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
            login(request, user)

            return redirect('user_details')

    context = {"form": form}
    return render(request, 'base/login_registration_page.html', context)


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

            profile_type = request.user.profile.profile_type
            print(profile_type)

            if profile_type == 'donor':
                return redirect('donor_home')
            elif profile_type == 'patient':
                return redirect('home')
            else:
                return redirect('donor_home')
        else:
            messages.error(request, "Email or Password is incorrect")

    context = {"page": page}
    return render(request, 'base/login_registration_page.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def UserDetails(request):
    form = UserDetailsForm()
    print(form)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)

        if form.is_valid():
            user_profile = request.user.profile

            user_profile.city = form.cleaned_data['city']
            user_profile.country = form.cleaned_data['country']
            user_profile.bloodgroup = form.cleaned_data['bloodgroup']
            user_profile.profile_type = form.cleaned_data['profile_type']

            user_profile.save()

            return redirect('home')

    context = {"form": form}

    return render(request, 'base/userDetails_page.html', context)


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


# //////////////////////////////////////////////////////////////////
# 2. DONORS PAGES
# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def DonorHome(request):
    page = 'home_donor_page'

    # blood_requests = Blood_Request.objects.all()

    # context = {'page': page, "blood_requests": blood_requests}
    context = {}
    return render(request, 'base/donor_homePage.html', context)


# //////////////////////////////////////////////////////////////////
# 3. PATIENTS PAGES
# //////////////////////////////////////////////////////////////////


@login_required(login_url='login')
def PatientHome(request):
    page = 'home_patient_page'

    context = {'page': page}
    return render(request, 'base/donor_PatientPage.html', context)
