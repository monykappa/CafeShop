from django.urls import include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import *
from django.urls import path
from django.contrib.auth import views as auth_views

from menu import views as menu_view
from . import views
from menu.views import *



app_name = 'menu'
urlpatterns = [
    re_path('menu/', views.menu, name='menu'),
    path('drink_details/<int:product_id>/', views.drink_details, name='drink_details'),
    path('order-details/', views.order_detail_list, name='order_detail_list'),
    path('order-details/<int:order_detail_id>/', views.order_detail_detail, name='order_detail_detail'),
    path('iced-drinks/', views.iced_drinks, name='IcedDrink'),
    path('hot-drinks/', views.hot_drinks, name='HotDrink'),
    path('frappe-drinks/', views.frappe_drinks, name='FrappeDrink'),
    path('add_to_order/', views.add_to_order, name='add_to_order'),
    path('cart/', views.cart, name='cart'),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('order_confirmation/', views.order_confirmation_page, name='order_confirmation_page'),
    path('remove_product_from_order/<int:order_detail_id>/', views.remove_product_from_order, name='remove_product_from_order')



]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)