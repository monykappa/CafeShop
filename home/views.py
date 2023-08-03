from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    templates = 'index.html'
    return render(request, templates)

def test(request):
    templates = 'test.html'
    return render(request, templates)
