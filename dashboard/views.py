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
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def dashboard(request):
    # Retrieve all products from the database
    products = AddProduct.objects.all()
    hot_drinks_count = AddProduct.objects.filter(product_name__icontains='Hot').count()
    iced_drinks_count = AddProduct.objects.filter(product_name__icontains='Iced').count()
    frappe_drinks_count = AddProduct.objects.filter(product_name__icontains='Frappe').count()


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
    # Get the product object based on the product_id
    product = get_object_or_404(AddProduct, pk=product_id)

    # Get the choices for the 'category' field directly from the model
    categories = AddProduct._meta.get_field('category').choices

    # Get the current page number from the session or default to 1
    current_page = request.GET.get('page', request.session.get('dashboard_current_page', 1))

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

        # Redirect back to the dashboard with the stored page number
        return HttpResponseRedirect(reverse('dashboard:dashboard') + f'?page={current_page}')

    # Render the edit product page for GET requests, passing the categories to the template
    return render(request, 'dashboard/admin/edit_product.html', {'product': product, 'categories': categories})


def delete_product(request, product_id):
    # Get the product object based on the product_id
    product = get_object_or_404(AddProduct, pk=product_id)

    # Perform the product deletion
    try:
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Error deleting product: {str(e)}'})


