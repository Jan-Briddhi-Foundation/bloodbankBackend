from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import CreateUserForm
# Create your views here.


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def loginPage(request):
    form = CreateUserForm()
    context = {"form": form}
    return render(request, 'base/anotherpage.html', context)


def registrationPage(request):
    context = {}
    return render(request, 'base/login_registration_page.html', context)
