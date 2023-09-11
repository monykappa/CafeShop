from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from userprofile.models import CustomerUser
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import OrderDetail
import logging
from .models import AddProduct, Size, ProductSize, OrderDetail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .forms import UserDetailForm




from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)


def user_detail(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            # Process the form data (save to the database, etc.)
            # You can access the user's location and contact as form.cleaned_data['location'] and form.cleaned_data['contact']
            
            # After processing, create a context with the order details and user data
            order_details = OrderDetail.objects.all()  # Query your OrderDetail model here
            user_data = {
                'location': form.cleaned_data['location'],
                'contact': form.cleaned_data['contact'],
            }
            context = {'order_details': order_details, 'user_data': user_data}
            
            # Redirect the user to the checkout page
            return render(request, 'checkout.html', context)
    else:
        form = UserDetailForm()

    return render(request, 'user_detail.html', {'form': form})

def checkout(request):
    # Render the checkout page with the order details and user data
    order_details = OrderDetail.objects.all()  # Query your OrderDetail model here
    user_data = {
        'location': request.POST.get('location'),  # Get the location from the POST data
        'contact': request.POST.get('contact'),    # Get the contact from the POST data
    }
    context = {'order_details': order_details, 'user_data': user_data}
    return render(request, 'Orderfolder/checkout.html', context)

def cart(request):
    if request.user.is_authenticated:
        # Retrieve order details associated with the user
        order_details = OrderDetail.objects.filter(user=request.user)

        # Debug: Print order_details to verify it contains the expected data
        print(order_details)

        return render(request, 'Orderfolder/cart.html', {'order_details': order_details})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponse("You must be signed in to view your cart.", status=401)





def remove_product_from_order(request, order_detail_id):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the current user
        user = request.user
        
        # Try to get the OrderDetail instance by its ID, and ensure it belongs to the current user
        order_detail = get_object_or_404(OrderDetail, pk=order_detail_id, user=user)
        
        # Delete the OrderDetail instance
        order_detail.delete()
        
        # Redirect to the cart or another appropriate page
        return redirect('menu:cart')  # Replace 'menu:cart' with your actual cart page URL

    # Handle invalid requests here (e.g., GET requests)
    return redirect('some_error_page')  # Replace 'some_error_page' with an error page URL

@login_required 
def cart_view(request):
    if request.user.is_authenticated:
        # Retrieve order details associated with the user
        order_details = OrderDetail.objects.filter(user=request.user)

        # Debug: Print order_details to verify it contains the expected data
        print(order_details)

        return render(request, 'Orderfolder/cart.html', {'order_details': order_details})
    else:
        # Handle the case where the user is not authenticated
        return HttpResponse("You must be signed in to view your cart.", status=401)


def add_to_order(request):
    if request.method == 'POST':
        # Get the selected size and quantity from the form
        selected_size_id = request.POST.get('selected_size')
        quantity = int(request.POST.get('quantity'))

        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Retrieve the selected product size
                selected_size = ProductSize.objects.get(pk=selected_size_id)

                # Create an order detail instance and associate it with the user
                order_detail = OrderDetail(
                    user=request.user,
                    product_size=selected_size,
                    quantity=quantity,
                )

                # Save the order detail
                order_detail.save()

                # Update the timestamp for the order detail after saving
                order_detail.order_time = timezone.now()
                order_detail.save()

                # Redirect the user to the 'menu' page
                return redirect('menu:menu')  # Redirect to the 'menu' page

            except ProductSize.DoesNotExist:
                # Handle the case where the selected product size does not exist
                return HttpResponse("Selected product size does not exist.", status=400)

        else:
            # Handle the case where the user is not authenticated
            return HttpResponse("You must be signed in to add to your order.", status=401)

    # Handle GET requests or other cases
    return HttpResponse("Invalid request.", status=400)



def drink_details(request, product_id):
    product = get_object_or_404(AddProduct, id=product_id)
    product_sizes = product.sizes.all()  # Get all sizes related to the product

    # Assuming you want to use the image URL of the first size
    if product_sizes:
        product_image_url = product_sizes[0].images.url
    else:
        product_image_url = None

    print("Product Image URL:", product_image_url)  # Debugging line

    return render(request, 'Orderfolder/drink_details.html', {'product': product})


def menu_view(request):
    if request.user.is_authenticated:
        cart_count = OrderDetail.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return render(request, 'Orderfolder/orderpage.html', {'cart_count': cart_count})

def menu(request):
    products = AddProduct.objects.all()
    grouped_products = {}

    # Group products by name
    for product in products:
        if product.product_name not in grouped_products:
            grouped_products[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_products[product.product_name]['sizes'].append(product.sizes.first())

    # Calculate cart count for the current user
    if request.user.is_authenticated:
        cart_count = OrderDetail.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Create a Paginator instance
    paginator = Paginator(list(grouped_products.values()), 20)  # Show 20 products per page

    page = request.GET.get('page')
    grouped_products_page = paginator.get_page(page)

    return render(request, 'Orderfolder/orderpage.html', {'grouped_products_page': grouped_products_page, 'cart_count': cart_count})

def iced_drinks(request):
    # Get all products with 'iced' in the product name
    iced_products = AddProduct.objects.filter(product_name__icontains='iced')
    
    grouped_iced_products = {}

    # Group iced products by name
    for product in iced_products:
        if product.product_name not in grouped_iced_products:
            grouped_iced_products[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_iced_products[product.product_name]['sizes'].append(product.sizes.first())

    # Create a Paginator instance
    paginator = Paginator(list(grouped_iced_products.values()), 5)  # Show 5 products per page

    page = request.GET.get('page')
    iced_products_page = paginator.get_page(page)

    return render(request, 'Orderfolder/iced_drinks.html', {'iced_products_page': iced_products_page})

def hot_drinks(request):
    # Get all products with 'hot' in the product name
    hot_products = AddProduct.objects.filter(product_name__icontains='Hot')
    
    grouped_hot_products = {}

    # Group hot products by name
    for product in hot_products:
        if product.product_name not in grouped_hot_products:
            grouped_hot_products[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_hot_products[product.product_name]['sizes'].append(product.sizes.first())

    # Create a Paginator instance
    paginator = Paginator(list(grouped_hot_products.values()), 5)  # Show 5 products per page

    page = request.GET.get('page')
    hot_products_page = paginator.get_page(page)

    return render(request, 'Orderfolder/hot_drinks.html', {'hot_products_page': hot_products_page})

def frappe_drinks(request):
    # Get all products with 'milkshake' or 'frappe' in the product name
    milkshake_products = AddProduct.objects.filter(product_name__icontains='milkshake')
    frappe_products = AddProduct.objects.filter(product_name__icontains='frappe')

    grouped_drinks = {}

    # Group milkshake products by name
    for product in milkshake_products:
        if product.product_name not in grouped_drinks:
            grouped_drinks[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_drinks[product.product_name]['sizes'].append(product.sizes.first())

    # Group frappe products by name
    for product in frappe_products:
        if product.product_name not in grouped_drinks:
            grouped_drinks[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_drinks[product.product_name]['sizes'].append(product.sizes.first())

    drinks = list(grouped_drinks.values())

    # Check if there are any drinks available
    if not drinks:
        return render(request, 'Orderfolder/no_drinks.html')

    # Create a Paginator instance
    paginator = Paginator(drinks, 5)  # Show 5 products per page

    page = request.GET.get('page')
    drinks_page = paginator.get_page(page)

    return render(request, 'Orderfolder/frappe_drinks.html', {'drinks_page': drinks_page})


# def select_size_view(request, product_id):
#     product = get_object_or_404(AddProduct, pk=product_id)

#     # You can retrieve the available sizes and prices for this product here
#     # and pass them to the template

#     return render(request, 'menu/select_size.html', {'product': product})

def order_detail_list(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_size_id = request.POST.get('product_size')
        quantity = request.POST.get('quantity')

        # Validate quantity (must be a positive integer)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, 'Quantity must be a positive integer.')
            return redirect('menu:menu')

        # Retrieve the selected product and size
        product = get_object_or_404(AddProduct, pk=product_id)
        size = get_object_or_404(Size, pk=product_size_id)

        # Retrieve the price for the selected product and size
        price = product.price

        # Calculate the total price based on the selected quantity and price
        total_price = price * quantity

        # Create an OrderDetail object with the selected options
        order_detail = OrderDetail.objects.create(
            product=product,
            size=size,
            quantity=quantity,
            total_price=total_price
        )

        # You can add additional logic here if needed

        # Redirect to a success page or another view
        return redirect('menu:order_detail_detail', order_detail_id=order_detail.id)


def order_detail_detail(request, order_detail_id):
    order_detail = OrderDetail.objects.get(pk=order_detail_id)
    # You can add additional logic here if needed
    return render(request, 'menu/order_detail_detail.html', {'order_detail': order_detail})



