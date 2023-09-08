from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    templates = 'dashboard/admin/dashboard.html'
    return render(request, templates)
