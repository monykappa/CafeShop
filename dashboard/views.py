from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import AddProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json

@login_required
def dashboard(request):
    # Retrieve all products from the database
    products = AddProduct.objects.all()
    
    # Create a Paginator instance
    paginator = Paginator(products, 5)  # Show 10 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    # Pass the paginated products to the template context
    context = {'products': products}
    
    return render(request, 'dashboard/admin/dashboard.html', context)


def edit_product(request, product_id):
    # Get the product object based on the product_id
    product = get_object_or_404(AddProduct, pk=product_id)

    # Get the choices for the 'category' field directly from the model
    categories = AddProduct._meta.get_field('category').choices

    if request.method == 'POST':
        # Update the product name, category, and size prices based on the form data
        new_product_name = request.POST.get('name')
        new_category = request.POST.get('category')

        product.product_name = new_product_name
        product.category = new_category

        # Update the price for each size based on the form data
        for size in product.sizes.all():
            new_price = request.POST.get(f'size_{size.id}')
            size.price = new_price
            size.save()  # Save the updated size

        # Save the updated product name, category, and size prices
        product.save()

        # Redirect back to the dashboard or any desired URL after saving
        return redirect('dashboard:dashboard')

    # Render the edit product page for GET requests, passing the categories to the template
    return render(request, 'dashboard/admin/edit_product.html', {'product': product, 'categories': categories})

def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            # Delete the product based on the product_id
            product = get_object_or_404(AddProduct, pk=product_id)
            product.delete()

            return JsonResponse({'message': 'Product deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Internal server error
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

