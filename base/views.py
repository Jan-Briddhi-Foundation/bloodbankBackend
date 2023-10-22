from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import Profile
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

    context = {'page': page}
    return render(request, 'base/login_registration_page.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def UserDetails(request):
    form = UserDetailsForm()
    print(form)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        print(form)

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
