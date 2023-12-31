from django.shortcuts import render
from userprofile.models import CustomerUser
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
from menu.models import Checkout, OrderDetail, OrderItem, ProductSize, AddProduct, CartItem, ProductSize
from datetime import datetime 


def checkout_view(request):
    # Retrieve the checkout data with related OrderDetail data, ordered by checkout ID in descending order
    checkout_data = Checkout.objects.select_related('user', 'customer').prefetch_related(
        'order_items__product_size__product'
    ).order_by('-checkout_id')

    # Create a list to store organized data by unique checkout IDs
    unique_checkouts = []

    for checkout in checkout_data:
        unique_checkout = {
            'checkout_id': checkout.checkout_id,
            'username': checkout.user.username,
            'products': [],
            'total_price': 0,  # Initialize total price
            'order_date': checkout.order_date,  # Include the 'order_date' field
        }
        for order_item in checkout.order_items.all():
            product = order_item.product_size.product
            if product:  # Check if there is a product
                total_price = order_item.product_size.price * order_item.quantity
                unique_checkout['products'].append({
                    'product_name': product.product_name,
                    'size': order_item.product_size.size.get_size_display(),
                    'quantity': order_item.quantity,
                    'price_per_unit': order_item.product_size.price,
                    'total_price': total_price,
                })
                unique_checkout['total_price'] += total_price  # Update total price
        unique_checkouts.append(unique_checkout)

    # Pass the data to the template
    context = {'user_checkouts': unique_checkouts}
    return render(request, 'dashboard/admin/checkout_data.html', context)

def display_customer_users(request):
    customer_users = CustomerUser.objects.all()
    return render(request, 'dashboard/admin/useraccount.html', {'customer_users': customer_users})


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
    paginator = Paginator(products, 10)  # Show 5 products per page

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
    product = get_object_or_404(AddProduct, id=product_id)

    if request.method == 'POST':
        # Retrieve the new category value from the POST data
        new_category = request.POST.get('category')

        # Update the product's category
        product.category = new_category

        # Save the updated product to the database
        product.save()

        # Get the size IDs from the POST data
        size_ids = request.POST.getlist('size_id')

        for size_id in size_ids:
            try:
                # Get the corresponding ProductSize instance
                product_size = ProductSize.objects.get(id=size_id)

                # Retrieve the new price value for the current size from the POST data
                new_price = request.POST.get(f'price_{size_id}')  # Assuming the input field names are 'price_[size_id]'

                # Update the product size price
                product_size.price = new_price

                # Save the updated product size to the database
                product_size.save()

            except ProductSize.DoesNotExist:
                messages.error(request, f"Product size with ID {size_id} not found.")

        # Add a success message
        messages.success(request, 'Changes saved successfully.')

        # Redirect to the product list page or another appropriate page
        return redirect('dashboard:dashboard')

    # Retrieve all possible category choices from the AddProduct model
    all_categories = [choice[1] for choice in AddProduct._meta.get_field('category').choices]

    # Retrieve all possible size choices from the Size model
    all_sizes = Size.SIZE_CHOICES

    return render(request, 'dashboard/admin/edit_product.html', {'product': product, 'all_categories': all_categories, 'all_sizes': all_sizes})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Disable CSRF protection for this view
def delete_product(request, product_id):
    if request.method == 'POST':  # Change the request method to POST
        # Get the product object based on the product_id
        product = get_object_or_404(AddProduct, pk=product_id)

        # Perform the product deletion
        try:
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting product: {str(e)}'})

    # Return an error response for non-POST requests
    return JsonResponse({'error': 'Invalid request method'})

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

