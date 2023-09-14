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
from menu.models import Checkout, OrderDetail, OrderItem, ProductSize, AddProduct, CartItem


def checkout_view(request):
    # Retrieve the checkout data with related OrderDetail data
    checkout_data = Checkout.objects.select_related('user', 'customer').prefetch_related(
        'order_items__product_size__product'
    )

    # Create a list to store organized data by unique checkout IDs
    unique_checkouts = []

    # Create a set to keep track of processed checkout IDs
    processed_checkouts = set()

    for checkout in checkout_data:
        checkout_id = checkout.checkout_id
        if checkout_id not in processed_checkouts:
            # Initialize data for this unique checkout ID
            unique_checkout = {
                'checkout_id': checkout_id,
                'username': checkout.user.username,
                'products': [],
                'total_price': 0,  # Initialize total price
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
            processed_checkouts.add(checkout_id)

    # Pass the data to the template
    context = {'user_checkouts': unique_checkouts}
    return render(request, 'dashboard/admin/checkout_data.html', context)





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

        # Add a success message
        messages.success(request, 'Changes saved successfully.')

        # Redirect to the product list page or another appropriate page
        return redirect('dashboard:dashboard')  # Replace with your URL pattern name

    # Retrieve all possible category choices from your model
    all_categories = [choice[1] for choice in AddProduct.category.field.choices]

    return render(request, 'dashboard/admin/edit_product.html', {'product': product, 'all_categories': all_categories})


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

