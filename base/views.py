from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import CreateUserForm
# Create your views here.


def registrationPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # login(request, user)

            instance = form.save(commit=False)
            instance.username = form.cleaned_data.get('email')
            user = instance.save()
            # login(request, user)

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
    context = {"form": form}
    return render(request, 'base/userDetails_page.html', context)


def home(request):
    context = {}
    return render(request, 'base/home.html', context)
