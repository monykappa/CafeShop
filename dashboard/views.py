from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import AddProduct, ProductSize, Size, OrderDetail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.utils import timezone
from django.db.models import Q 
from django import forms

@login_required
def dashboard(request):
    # Retrieve all products from the database
    products = AddProduct.objects.all()
    hot_drinks_count = AddProduct.objects.filter(product_name__icontains='Hot').count()
    iced_drinks_count = AddProduct.objects.filter(product_name__icontains='Iced').count()
    frappe_drinks_count = AddProduct.objects.filter(
        Q(product_name__icontains='Frappe') | Q(product_name__icontains='Milkshake')
    ).count()

    total_drinks_count = products.count()  # Total count of all drinks

    context = {
        'products': products,
        'hot_drinks_count': hot_drinks_count,
        'iced_drinks_count': iced_drinks_count,
        'frappe_drinks_count': frappe_drinks_count,
        'total_drinks_count': total_drinks_count,  # Add total drinks count to context
    }

    # Create a Paginator instance
    paginator = Paginator(products, 5)  # Show 5 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    # Store the current page number in the session
    request.session['dashboard_current_page'] = products.number

    # Pass the paginated products and the context to the template
    context['products'] = products

    return render(request, 'dashboard/admin/dashboard.html', context)







def edit_product(request, product_id):
    # Get the product based on the provided product_id
    product = get_object_or_404(AddProduct, id=product_id)

    if request.method == 'POST':
        # Handle form submissions here if necessary
        # ...

        # After processing, you might want to redirect the user to a different page
        # For example, after updating the product, you can redirect to the product list page
        return redirect('dashboard:product_list')  # Replace 'product_list' with the name of your product list view

    # If it's a GET request, render the edit_product.html template with the product
    return render(request, 'dashboard/admin/edit_product.html', {'product': product})



def delete_product(request, product_id):
    # Get the product object based on the product_id
    product = get_object_or_404(AddProduct, pk=product_id)

    # Perform the product deletion
    try:
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Error deleting product: {str(e)}'})

def add_new_product_view(request):
    sizes = Size.objects.all()  # Retrieve all size choices from the database
    # Retrieve category choices from the model
    category_choices = [(choice, choice) for choice, _ in AddProduct._meta.get_field('category').choices]

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')

        # Create a new product using the data
        new_product = AddProduct(product_name=product_name, category=category)
        new_product.save()

        # Handle multiple sizes, prices, and images
        for size in sizes:
            size_id = request.POST.get(f'size_{size.id}')
            price = request.POST.get(f'price_{size.id}')
            image = request.FILES.get(f'image_{size.id}')

            if size_id and price:
                # Retrieve the Size instance based on the size_id
                size_instance = Size.objects.get(id=size_id)

                # Create the ProductSize instance with the Size instance
                product_size = ProductSize(product=new_product, size=size_instance, price=price, images=image)
                product_size.save()

        return redirect('dashboard:dashboard')  # Redirect to the dashboard home page

    context = {'sizes': sizes, 'category_choices': category_choices}
    return render(request, 'dashboard/admin/addproduct.html', context)

def order_detail_view(request):
    # Retrieve the order details and create a Paginator instance
    current_time = timezone.localtime(timezone.now())
    order_details = OrderDetail.objects.all()
    paginator = Paginator(order_details, 10)  # Show 10 items per page

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'dashboard/admin/order_detail.html', {'order_details': page, 'current_time': current_time})

