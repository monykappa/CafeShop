from django.urls import include, re_path
from django.conf import settings 
from django.conf.urls.static import static
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views

from dashboard import views as dashboard_view
from . import views
from dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    re_path('^dashboard/$', dashboard_view.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    