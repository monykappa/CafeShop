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
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied


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



@login_required
def delete_profile_picture(request):
    if request.method == 'POST':
        user = request.user
        try:
            customer_user = CustomerUser.objects.get(user=user)
            
            # Check if the user has the necessary permissions to delete their profile picture
            if customer_user.user != user:
                raise PermissionDenied
            
            if customer_user.profile_image:
                customer_user.profile_image.delete()  # Delete the profile picture file
                customer_user.save()  # Save the changes
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Profile picture not found.'})
        except CustomerUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
        except PermissionDenied:
            return JsonResponse({'success': False, 'message': 'Permission denied.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




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



