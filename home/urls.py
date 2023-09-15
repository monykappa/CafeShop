from django.urls import include, re_path, path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views

from home import views as home_view
from . import views
from home.views import *

from userprofile import views as userprofile_view
from . import views
from userprofile.views import *

app_name = 'home'
urlpatterns = [
  re_path('^index/$', home_view.index, name='index'),
    re_path('^home/$', home_view.home, name='home'),
    re_path('^test/$', home_view.test, name='test'),
    re_path('^aboutus/$', home_view.aboutus, name='aboutus'),
    re_path('^findus/$', home_view.FindUs, name='findus'),
    re_path('^drinks/$',home_view.drinks,name='drinkpage'),
    re_path('^hottea/$',home_view.hottea,name='hotcoffee'),
    re_path('^profile/$', home_view.profile, name='profile'),
    re_path('^favoritedrinks/$', home_view.favdrink, name='favoritedrink'),
    re_path('^previousorder/$', home_view.previousorder, name='previousorder'),
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('delete_profile_picture/', views.delete_profile_picture, name='delete_profile_picture'),
    # path('edit_user_info/', views.edit_user_info, name='edit_user_info'),
    # path('update_profile_info/', views.update_profile_info, name='update_profile_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    