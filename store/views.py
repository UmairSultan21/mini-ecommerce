from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# -------- BASIC PAGES --------
def home(request):
    return render(request, "home.html")

def products(request):
    return render(request, "products.html")

def orders(request):
    return render(request, "orders.html")


# -------- ROLE CHECK FUNCTION --------
def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if getattr(request.user, 'role', None) != role:
                return redirect('login')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# -------- ROLE BASED HOME PAGES --------

@login_required
def user_home(request):
    return render(request, "store/user_home.html")


@login_required
def seller_home(request):
    return render(request, "store/seller_home.html")


@login_required
def admin_home(request):
    return render(request, "store/admin_home.html")