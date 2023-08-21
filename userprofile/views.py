from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView 
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from userprofile.models import SignUp
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import UserProfile  

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class SigninView(View):
    def get(self, request):
        template_name = 'dashboard/userprofile/signin.html'
        return render(request, template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user (you should customize this logic)
        user = authenticate(request, username=username, password=password)
        
        

        if user is not None:
            # Authentication successful, log in the user
            login(request, user)
            return redirect('home:home')
        else:
            # Authentication failed, display an error message
            context = {'login_failed': True}
            template_name = 'dashboard/userprofile/signin.html'
            return render(request, template_name, context)

    # def get(self, request):
    #     return render(request, self.template_name)

    # def post(self, request, *args, **kwargs):
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')

    #     print(f"Received username: {username}")
    #     print(f"Received password: {password}")

    #     # Authenticate the user
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         # If authentication is successful, log in the user
    #         login(request, user)
    #         print(f"User authenticated: {user.username}")
    #         return redirect('home:home')
    #     else:
    #         # If authentication fails, display an error message
    #         print(f"Authentication failed for username: {username}")
    #         context = {'login_failed': True}
    #         return render(request, self.template_name, context)

class SignupView(View):
    template_name = 'dashboard/userprofile/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Retrieve data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')

        # Create a new User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create a new SignUp instance linked to the User
        signup = SignUp(
            user=user,
            email=email,
            username=username,
            password=password,
            sex=sex,
            dob=dob,
            contact=contact
        )

        # Save the SignUp instance
        signup.save()

        # Authenticate the user and log them in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('userprofile:signin')



class LogoutView(View):
    def get(self, request): 
        logout(request)
        return redirect('home:index')
