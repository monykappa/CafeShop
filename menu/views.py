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
from .models import AddProduct, Size

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

def drink_details(request, product_id):
    # Retrieve the product based on the product_id
    product = get_object_or_404(AddProduct, pk=product_id)
    
    # Add your logic here to render the drink details page
    # You can pass the 'product' to the template
    
    return render(request, 'Orderfolder/drink_details.html', {'product': product})

def menu(request):
    # Fetch distinct product names
    distinct_product_names = AddProduct.objects.values('product_name').distinct()

    # Create a dictionary to hold product information
    product_info = {}

    for product_name in distinct_product_names:
        # Get the first product with this name
        product = AddProduct.objects.filter(product_name=product_name['product_name']).first()

        if product:
            # Add the product to the dictionary using its name as the key
            product_info[product_name['product_name']] = product

    # Render the menu.html template with the product data
    return render(request, 'Orderfolder/orderpage.html', {'product_info': product_info})


def select_size_view(request, product_id):
    product = get_object_or_404(AddProduct, pk=product_id)

    # You can retrieve the available sizes and prices for this product here
    # and pass them to the template

    return render(request, 'menu/select_size.html', {'product': product})

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



