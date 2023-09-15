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
from userprofile.models import CustomerUser
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
import os
import logging

def favdrink(request):
    templates='favoriteproduct.html'
    return render(request,templates)
def previousorder(request):
    templates='previousorder.html'
    return render(request,templates)
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

from datetime import datetime
# def edit_user_info(request):
#     user = request.user

#     if request.method == 'POST':
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname')
#         email = request.POST.get('email')
#         profile_image = request.FILES.get('profile_image')

#         # Use a database transaction to ensure both models are updated or none at all
#         with transaction.atomic():
#             try:
#                 # Update CustomerUser model if user is a Customer
#                 if hasattr(user, 'customeruser'):
#                     customer_user = user.customeruser
#                     customer_user.firstname = firstname
#                     customer_user.lastname = lastname
#                     customer_user.email = email
#                     if profile_image:
#                         customer_user.profile_image = profile_image
#                     customer_user.save()

#                 # Update Staff model if user is a Staff
#                 elif hasattr(user, 'staff'):
#                     staff = user.staff
#                     staff.firstname = firstname
#                     staff.lastname = lastname
#                     staff.email = email
#                     staff.save()

#                 user.first_name = firstname
#                 user.last_name = lastname
#                 user.email = email
#                 user.save()

#                 messages.success(request, 'Profile updated successfully.')
#                 return redirect('home:profile')

#             except Exception as e:
#                 # Handle any exceptions that may occur during the update
#                 messages.error(request, 'An error occurred while updating your profile.')
#                 print(str(e))

#     return render(request, 'dashboard/userprofile/edit_user_info.html', {'user': user})






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


@csrf_exempt
def update_profile_picture(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('profile_image')

        if uploaded_file:
            user = request.user
            customer_user = user.customeruser  # Replace with your actual model name
            customer_user.profile_image = uploaded_file
            customer_user.save()
            return JsonResponse({'message': 'Profile picture updated successfully'})
        else:
            return JsonResponse({'error': 'No profile image provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




from django.urls import reverse

def delete_profile_picture(request):
    if request.method == 'POST':
        try:
            user_profile = CustomerUser.objects.get(user=request.user)
        except CustomerUser.DoesNotExist:
            user_profile = None

        if user_profile:
            if user_profile.profile_image:
                # Delete the profile image file
                user_profile.profile_image.delete()

                # Set the 'profile_image' field to None to clear the reference
                user_profile.profile_image = None
                user_profile.save()

                messages.success(request, 'Profile picture deleted successfully.')
            else:
                messages.error(request, 'No profile picture to delete.')
        else:
            messages.error(request, 'User profile not found.')

    return redirect(reverse('home:profile'))









@login_required
def profile(request):
    user = request.user

    try:
        customer_user = CustomerUser.objects.get(user=user)
    except CustomerUser.DoesNotExist:
        customer_user = None

    # Query the checkout history for the user
    checkout_history = Checkout.objects.filter(customer=user.customer).order_by('order_date')

    # Group the checkout items by date and time
    grouped_checkouts = {}
    for checkout in checkout_history:
        key = checkout.order_date.strftime('%d-%B-%Y %I:%M %p')
        if key in grouped_checkouts:
            grouped_checkouts[key]['order_items'].extend(checkout.order_items.all())
        else:
            grouped_checkouts[key] = {'order_date': checkout.order_date, 'order_items': list(checkout.order_items.all())}

    # Calculate the total price for each checkout group
    for group in grouped_checkouts.values():
        total_price = 0
        for order_item in group['order_items']:
            total_price += order_item.product_size.price
        group['total_price'] = total_price

    context = {
        'user': user,
        'customer_user': customer_user,
        'grouped_checkouts': grouped_checkouts.values(),
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



