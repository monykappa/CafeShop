from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userprofile.models import SignUp 


def index(request):
    templates = 'index.html'
    return render(request, templates)

def test(request):
    templates = 'test.html'
    return render(request, templates)

@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            signup_user = SignUp.objects.get(email=user.email)
            username = signup_user.username
        except SignUp.DoesNotExist:
            username = None
    else:
        username = None

    context = {'username': username}
    return render(request, 'home.html', context)

def aboutus(request):
    templates = 'aboutus.html'
    return render(request, templates)


