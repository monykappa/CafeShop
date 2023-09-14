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
from userprofile.models import *
import logging
from .models import AddProduct, Size, ProductSize, OrderDetail, CartItem, OrderItem
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Checkout
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum, F, ExpressionWrapper, DecimalField







from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

def register_user(request):
    # Your registration logic here, e.g., creating a User object

    # After creating the User object, create a related Customer object
    customer = Customer.objects.create(user=user, location='', contact='')

    # Save the customer object
    customer.save()

    # Redirect to the User Detail page or wherever needed

def user_detail(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        district = request.POST.get('district')
        house_number = request.POST.get('house_number')
        road = request.POST.get('road')
        contact = request.POST.get('contact')
        
        # Update the district, house_number, road, and contact information
        customer.district = district
        customer.house_number = house_number
        customer.road = road
        customer.contact = contact
        customer.save()
        
        return redirect('menu:checkout')

    return render(request, 'Orderfolder/user_detail.html', {'customer': customer, 'DistrictChoices': DistrictChoices})

def continue_to_order(request):
    if request.user.is_authenticated:
        # Retrieve cart items associated with the user
        cart_items = CartItem.objects.filter(user=request.user)

        for cart_item in cart_items:
            # Create an OrderDetail object from the cart item
            order_detail = OrderDetail(
                user=request.user,
                product_size=cart_item.product_size,
                quantity=cart_item.quantity,
            )
            order_detail.save()

        # Clear the user's cart by deleting cart items
        cart_items.delete()

        # Redirect to user_detail or the desired page
        return redirect('menu:user_detail')

    else:
        # Handle the case where the user is not authenticated
        return HttpResponse("You must be signed in to continue to order.", status=401)
    

@login_required
def initiate_checkout(request):
    if request.user.is_authenticated:
        # Create a new Checkout instance for the user
        checkout = Checkout.objects.create(
            customer=request.user.customer,
            user=request.user,
        )

        # Redirect the user to the new checkout
        return redirect('menu:checkout')  # Change 'menu:checkout' to your actual checkout URL
    else:
        return HttpResponse("You must be signed in to initiate a checkout.", status=401)


@login_required
def checkout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Assuming you have a form or a button to initiate the checkout process
            # Here, we'll assume you have a button with name="checkout" in your template
            if 'checkout' in request.POST:
                # Retrieve cart items associated with the user
                cart_items = CartItem.objects.filter(user=request.user)

                # Create OrderDetail objects from cart items and associate them with the user
                for cart_item in cart_items:
                    OrderDetail.objects.create(
                        user=request.user,
                        product_size=cart_item.product_size,
                        quantity=cart_item.quantity,
                    )

                # Clear the cart by deleting cart items
                cart_items.delete()

                # Redirect the user to the 'checkout' page or a confirmation page
                return redirect('menu:checkout')  # Change 'menu:checkout' to your actual checkout URL

        # Retrieve order details associated with the user
        order_details = OrderDetail.objects.filter(user=request.user)

        # Calculate the total price
        total_price = Decimal(0)
        for order_detail in order_details:
            total_price += order_detail.total_price

        # Assuming you have a Customer model to store location and contact
        customer = request.user.customer  # Assuming a one-to-one relationship between User and Customer

        return render(request, 'Orderfolder/checkout.html', {'order_details': order_details, 'user': request.user, 'customer': customer, 'total_price': total_price})
    else:
        return HttpResponse("You must be signed in to view the checkout page.", status=401)

    
@login_required
def confirm_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Get the current user
            user = request.user

            # Retrieve OrderDetail instances for the current user
            order_details = OrderDetail.objects.filter(user=user)

            # Create a Checkout instance with a unique identifier
            checkout = Checkout.objects.create(
                customer=user.customer,
                user=user
            )

            # Create OrderItem instances for each OrderDetail and associate them with the Checkout
            for order_detail in order_details:
                order_item, _ = OrderItem.objects.get_or_create(
                    product_size=order_detail.product_size,
                    defaults={'quantity': order_detail.quantity}
                )
                checkout.order_items.add(order_item)

            # Delete the OrderDetail instances for the current user
            order_details.delete()

            # Redirect to the 'order_confirmation_page' URL or wherever you want
            return redirect('menu:order_confirmation_page')

    return HttpResponse("Invalid request method", status=405)













def order_confirmation_page(request):
    return render(request, 'Orderfolder/order_confirmation.html')


def cart(request):
    if request.user.is_authenticated:
        # Count the number of items in the user's cart (CartItems)
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        # User is not authenticated, cart count is 0
        cart_count = 0

    # Retrieve cart items associated with the user from the CartItem model
    cart_items = CartItem.objects.filter(user=request.user)

    return render(request, 'Orderfolder/cart.html', {'cart_items': cart_items, 'cart_count': cart_count})




def remove_product_from_order(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.delete()
            return HttpResponse(status=200)  # Return a success response
        except CartItem.DoesNotExist:
            return HttpResponse(status=404)  # Return a not found response

    return HttpResponse(status=400)  # Return a bad request response

@login_required 
def cart_view(request):
    if request.user.is_authenticated:
        # Count the number of items in the user's cart (CartItems)
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        # User is not authenticated, cart count is 0
        cart_count = 0

    # Retrieve cart items associated with the user from the CartItem model
    cart_items = CartItem.objects.filter(user=request.user)

    return render(request, 'Orderfolder/cart.html', {'cart_items': cart_items, 'cart_count': cart_count})


def add_to_cart(request):
    if request.method == 'POST':
        selected_size_id = request.POST.get('selected_size')
        quantity = int(request.POST.get('quantity'))

        if request.user.is_authenticated:
            try:
                selected_size = ProductSize.objects.get(pk=selected_size_id)
                
                # Check if a cart item with the same product size already exists for the user
                cart_item, created = CartItem.objects.get_or_create(
                    user=request.user,
                    product_size=selected_size,
                    defaults={'quantity': 0}  # Create with quantity 0 if it doesn't exist
                )

                # Update the quantity by adding the new quantity
                cart_item.quantity += quantity
                cart_item.save()

                return redirect('menu:menu')  # Redirect to the 'menu' page

            except ProductSize.DoesNotExist:
                return HttpResponse("Selected product size does not exist.", status=400)

        else:
            return HttpResponse("You must be signed in to add to your cart.", status=401)

    return HttpResponse("Invalid request.", status=400)


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

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Pass 'cart_count' as part of the context
    context = {
        'product': product,
        'product_image_url': product_image_url,
        'cart_count': cart_count,  # Include cart_count in the context
    }

    return render(request, 'Orderfolder/drink_details.html', context)


def menu_view(request):
    if request.user.is_authenticated:
        # Calculate cart count based on CartItem model
        cart_count = CartItem.objects.filter(user=request.user).count()
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

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Create a Paginator instance
    paginator = Paginator(list(grouped_products.values()), 30) 
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

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Create a Paginator instance
    paginator = Paginator(list(grouped_iced_products.values()), 10)

    page = request.GET.get('page')
    iced_products_page = paginator.get_page(page)

    # Pass 'cart_count' as part of the context
    context = {
        'iced_products_page': iced_products_page,
        'cart_count': cart_count,  # Include cart_count in the context
    }

    return render(request, 'Orderfolder/iced_drinks.html', context)


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
    paginator = Paginator(list(grouped_hot_products.values()), 10)  

    page = request.GET.get('page')
    hot_products_page = paginator.get_page(page)

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Pass 'cart_count' as part of the context
    context = {
        'hot_products_page': hot_products_page,
        'cart_count': cart_count,  # Include cart_count in the context
    }

    return render(request, 'Orderfolder/hot_drinks.html', context)


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
    paginator = Paginator(drinks, 10)  

    page = request.GET.get('page')
    drinks_page = paginator.get_page(page)

    # Calculate cart count based on CartItem model for the current user
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0  # User is not authenticated, cart count is 0

    # Pass 'cart_count' as part of the context
    context = {
        'drinks_page': drinks_page,
        'cart_count': cart_count,  # Include cart_count in the context
    }

    return render(request, 'Orderfolder/frappe_drinks.html', context)




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



