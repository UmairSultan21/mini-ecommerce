from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

User = get_user_model()


# -------- LOGIN --------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Validate input
        if not email or not password:
            messages.error(request, "Please enter both email and password")
            return render(request, "users/login.html")

        # 2. Get user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, "users/login.html")

        # 3. Authenticate
        auth_user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if auth_user is not None:
            login(request, auth_user)

            # 4. Role-based redirect (FIXED)
            if auth_user.is_superuser:
                return redirect('admin_home')

            role = getattr(auth_user, 'role', None)

            if role == 'seller':
                return redirect('seller_home')

            if role == 'customer':
                return redirect('user_home')

            # fallback
            return redirect('user_home')

        messages.error(request, "Invalid email or password")
        return render(request, "users/login.html")

    return render(request, "users/login.html")

# -------- REGISTER --------
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "users/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "users/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "users/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # save role safely (ONLY if your model has it)
        if hasattr(user, 'role'):
            user.role = role
            user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "users/register.html")


# -------- OTHER PAGES --------
def forgot_password(request):
    return render(request, "users/forgot_password.html")


def profile(request):
    return render(request, "users/profile.html")


def edit_profile(request):
    return render(request, "users/edit_profile.html")