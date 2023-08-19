from django.contrib.auth.backends import ModelBackend
from .models import SignUp

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = SignUp.objects.get(username=username)
            if user.check_password(password):
                return user
        except SignUp.DoesNotExist:
            return None
