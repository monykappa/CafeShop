from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from userprofile.models import SignUp
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from userprofile.models import SignUp
from django.urls import reverse




from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



class SigninView(View):
    template_name = 'dashboard/userprofile/signin.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated:", user.username)
            login(request, user)
            return redirect('home:home')
        else:
            context = {'login_failed': True}
            return render(request, self.template_name, context)

        
class SignupView(View):
    template_name = 'dashboard/userprofile/signup.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        
        user = SignUp.objects.create_user(
            email=email, 
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            sex=sex,
            dob=dob,
            contact=contact
        )
        
        # Authenticate and login the user after signup
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        
        return redirect('userprofile:signin')  # Redirect to the sign-in page

    

class LogoutView(View):
    def get(self, request): 
        logout(request)
        return redirect('home:index')
