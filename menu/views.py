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
from userprofile.models import SignUp
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import OrderDetail
import logging
from .models import Product, Size, ProductPrice

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

def menu(request):
    # Retrieve a list of products from the database
    products = Product.objects.all()

    # Render the menu.html template with the product data
    return render(request, 'menu/menu.html', {'products': products})

def select_size_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # You can retrieve the available sizes and prices for this product here
    # and pass them to the template

    return render(request, 'menu/select_size.html', {'product': product})

def order_detail_list(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_price_id = request.POST.get('product_size')
        quantity = request.POST.get('quantity')

        # Validate quantity (must be a positive integer)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, 'Quantity must be a positive integer.')
            return redirect('menu:menu')

        # Retrieve the selected product and price
        product = get_object_or_404(Product, pk=product_id)
        product_price = get_object_or_404(ProductPrice, pk=product_price_id)

        # Calculate the total price based on the selected quantity and price
        total_price = product_price.price * quantity

        # Create an OrderDetail object with the selected options
        order_detail = OrderDetail.objects.create(
            product_price=product_price,
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



