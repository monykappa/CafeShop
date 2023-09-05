from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userprofile.models import User


def index(request):
    templates = 'index.html'
    return render(request, templates)

def test(request):
    templates = 'test.html'
    return render(request, templates)

def drinks(request):
    return render(request,'Orderfolder/orderpage.html')
def hottea(request):
    return render(request,'Orderfolder/hottea.html')
@login_required
def home(request):
    context = {'username': request.user.username}
    return render(request, 'home.html', context)

def aboutus(request):
    templates = 'aboutus.html'
    return render(request, templates)

def FindUs(request):
    templates = 'location/find_us.html'
    return render(request, templates)


