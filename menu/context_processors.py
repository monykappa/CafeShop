# menu/context_processors.py

from .models import OrderDetail  # Import your OrderDetail model or any necessary models

def cart_count(request):
    if request.user.is_authenticated:
        cart_count = OrderDetail.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
