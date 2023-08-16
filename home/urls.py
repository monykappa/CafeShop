from django.urls import include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import DetailView

from home import views as home_view
from . import views
from home.views import *

app_name = 'home'
urlpatterns = [
    re_path('^home/$', home_view.home, name='home'),
    re_path('^test/$', home_view.test, name='test'),
    re_path('^aboutus/$', home_view.aboutus,name='aboutus'),
   
]