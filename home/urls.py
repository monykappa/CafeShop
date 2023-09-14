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
    re_path('profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    