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
from userprofile.models import CustomerUser
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import CustomerUser, Sex 

from .models import Customer  

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
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')

        # Retrieve the profile image file from the request
        profile_image = request.FILES.get('profile_image')

        # Create a new User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create a new CustomerUser instance linked to the User
        customer_user = CustomerUser(
            user=user,
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            sex=sex,
            dob=dob,
            profile_image=profile_image  # Associate the profile image with the CustomerUser
        )

        # Save the CustomerUser instance
        customer_user.save()

        # Authenticate the user and log them in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('home:home')



class LogoutView(View):
    def get(self, request): 
        logout(request)
        return redirect('home:index')

