from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import AddProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


