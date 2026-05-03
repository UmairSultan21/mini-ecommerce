from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, CartItem, Wishlist


# =========================================================
# BASIC PAGES
# =========================================================

def home(request):
    products = Product.objects.all().order_by('-id')
    return render(request, "home.html", {"products": products})


def products(request):
    return render(request, "products.html")


def orders(request):
    return render(request, "orders.html")


# =========================================================
# ADD PRODUCT (SELLER)
# =========================================================

@login_required(login_url='login')
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        if Product.objects.filter(name=name, category=category).exists():
            messages.warning(request, "Product already exists in this category!")
            return redirect("add_product")

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            category=category,
            image=image
        )

        messages.success(request, "Product added successfully!")
        return redirect("seller_home")

    return render(request, "store/add_product.html")


# =========================================================
# HELPERS
# =========================================================

def _get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def _cart_count(user):
    return _get_cart(user).items.count()


def _wishlist_count(user):
    return Wishlist.objects.filter(user=user).count()


def _order_count(user):
    try:
        return user.orders.count()
    except:
        return 0


# =========================================================
# USER HOME
# =========================================================

@login_required(login_url='login')
def user_home(request):
    products = Product.objects.all().order_by('-id')[:20]

    wishlisted_ids = Wishlist.objects.filter(
        user=request.user
    ).values_list('product_id', flat=True)

    return render(request, "store/user_home.html", {
        "products": products,
        "wishlisted_ids": set(wishlisted_ids),

        "cart_count": _cart_count(request.user),
        "wishlist_count": _wishlist_count(request.user),
        "order_count": _order_count(request.user),
    })


# =========================================================
# ROLE PAGES
# =========================================================

@login_required(login_url='login')
def seller_home(request):
    return render(request, "store/seller_home.html")


@login_required(login_url='login')
def admin_home(request):
    return render(request, "store/admin_home.html")


# =========================================================
# CART
# =========================================================

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, "Product added/updated in cart.")
    return redirect(request.META.get('HTTP_REFERER', 'user_home'))


@login_required(login_url='login')
def cart_page(request):
    cart = _get_cart(request.user)

    cart_items = CartItem.objects.filter(
        cart=cart
    ).select_related('product')

    return render(request, "store/user_cart.html", {
        "cart_items": cart_items
    })


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = _get_cart(request.user)

    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

    messages.info(request, "Item removed from cart.")
    return redirect('user_cart')


# =========================================================
# WISHLIST
# =========================================================

@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item = Wishlist.objects.filter(user=request.user, product=product).first()

    if item:
        item.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER', 'user_home'))


@login_required(login_url='login')
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    return render(request, "store/user_wishlist.html", {
        "wishlist_items": wishlist_items
    })