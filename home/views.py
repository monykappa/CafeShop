from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userprofile.models import User
from menu.models import *
from userprofile.models import *


def index(request):
    templates = 'index.html'
    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)


def test(request):
    templates = 'test.html'

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)

def drinks(request):
    templates = 'Orderfolder/orderpage.html'

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)

def hottea(request):
    templates = 'Orderfolder/hottea.html'

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)


@login_required
def home(request):
    context = {'username': request.user.username}

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context['cart_count'] = cart_count  # Include cart_count in the context

    return render(request, 'home.html', context)

@login_required
def profile(request):
    user = request.user

    try:
        customer_user = CustomerUser.objects.get(user=user)
    except CustomerUser.DoesNotExist:
        customer_user = None

    checkout_history = Checkout.objects.filter(customer=user.customer)

    context = {
        'user': user,
        'customer_user': customer_user,
        'checkout_history': checkout_history,
    }

    return render(request, 'dashboard/userprofile/profile.html', context)


def aboutus(request):
    templates = 'aboutus.html'

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)


def FindUs(request):
    templates = 'location/find_us.html'

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    context = {'cart_count': cart_count}  # Include cart_count in the context

    return render(request, templates, context)



