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
from .models import AddProduct, Size, ProductSize
from django.core.paginator import Paginator



from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

def drink_details(request, product_id):
    product = get_object_or_404(AddProduct, id=product_id)
    return render(request, 'Orderfolder/drink_details.html', {'product': product})

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

    # Create a Paginator instance
    paginator = Paginator(list(grouped_products.values()), 6)  # Show 5 products per page

    page = request.GET.get('page')
    grouped_products_page = paginator.get_page(page)

    return render(request, 'Orderfolder/orderpage.html', {'grouped_products_page': grouped_products_page})

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
    hot_products = AddProduct.objects.filter(product_name__icontains='hot')
    
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
    # Get all products with 'frappe' in the product name
    frappe_products = AddProduct.objects.filter(product_name__icontains='frappe')
    
    grouped_frappe_products = {}

    # Group frappe products by name
    for product in frappe_products:
        if product.product_name not in grouped_frappe_products:
            grouped_frappe_products[product.product_name] = {
                'id': product.id,
                'product_name': product.product_name,
                'sizes': [],
            }
        grouped_frappe_products[product.product_name]['sizes'].append(product.sizes.first())

    # Create a Paginator instance
    paginator = Paginator(list(grouped_frappe_products.values()), 5)  # Show 5 products per page

    page = request.GET.get('page')
    frappe_products_page = paginator.get_page(page)

    return render(request, 'Orderfolder/frappe_drinks.html', {'frappe_products_page': frappe_products_page})


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



