from django.urls import include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import *
from django.urls import path
from django.contrib.auth import views as auth_views

from userprofile import views as userprofile_view
from . import views
from userprofile.views import *

app_name = 'userprofile'    
urlpatterns = [
    # url('^home/$', staff_view.home_page, name='home'),
<<<<<<< HEAD
    re_path('^signin/$', SigninView.as_view(), name='signin'),
    re_path('signup/', SignupView.as_view(), name='signup'),
    re_path('^logout/$', LogoutView.as_view(), name='logout'),
    # re_path('^feature/$',)
=======
    re_path(r'^signin/$', SigninView.as_view(), name='signin'), 
    re_path(r'^signup/$', SignupView.as_view(), name='signup'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),  

>>>>>>> 36944d2e61aa2a88a99fd06b62ddbe23e3d752d1
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
