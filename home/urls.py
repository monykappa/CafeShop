from django.urls import include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views

from home import views as home_view
from . import views
from home.views import *

app_name = 'home'
urlpatterns = [
    re_path('^index/$', home_view.index, name='index'),
    re_path('^home/$', home_view.home, name='home'),
    re_path('^test/$', home_view.test, name='test'),
    re_path('^aboutus/$', home_view.aboutus,name='aboutus'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)