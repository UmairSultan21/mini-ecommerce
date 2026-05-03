from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product


# -------- BASIC PAGES --------
def user_home(request):
    products = Product.objects.all().order_by('-id')[:20]  # latest 20 products

    return render(request, "store/user_home.html", {
        "products": products
    })

def home(request):
    products = Product.objects.all().order_by('-id')  # ALL products

    return render(request, "home.html", {
        "products": products
    })

def products(request):
    return render(request, "products.html")

def orders(request):
    return render(request, "orders.html")

def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        # 🔥 DUPLICATE CHECK (same name + category)
        if Product.objects.filter(name=name, category=category).exists():
            messages.warning(request, "⚠ Product already exists in this category!")
            return redirect("add_product")

        try:
            Product.objects.create(
                name=name,
                price=price,
                description=description,
                category=category,
                image=image
            )

            messages.success(request, "✅ Product added successfully!")
            return redirect("seller_home")

        except Exception as e:
            messages.error(request, f"❌ Error adding product: {str(e)}")
            return redirect("add_product")

    return render(request, "store/add_product.html")


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

# @login_required
# def user_home(request):
#     return render(request, "store/user_home.html")


@login_required
def seller_home(request):
    return render(request, "store/seller_home.html")


@login_required
def admin_home(request):
    return render(request, "store/admin_home.html")


from django.shortcuts         import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib           import messages
from .models                  import Product, Cart, CartItem, Wishlist


# ─────────────────────────────────────────
#  HELPER — get cart item count for navbar
# ─────────────────────────────────────────
def _cart_count(user):
    """Returns total item count in user's cart (0 if no cart yet)."""
    try:
        return user.cart.total_items()
    except Cart.DoesNotExist:
        return 0


def _wishlist_count(user):
    return user.wishlist.count()


def _order_count(user):
    """Will use Order model once orders app is wired up."""
    try:
        return user.orders.count()
    except Exception:
        return 0


# ─────────────────────────────────────────
#  USER HOME — top 20 latest products
# ─────────────────────────────────────────
@login_required(login_url='login')
def user_home(request):
    products = Product.objects.all().order_by('-id')[:20]

    # IDs the user has already wishlisted (to toggle heart icon)
    wishlisted_ids = set(
        Wishlist.objects.filter(user=request.user)
                        .values_list('product_id', flat=True)
    )

    context = {
        'products':       products,
        'wishlisted_ids': wishlisted_ids,
        'cart_count':     _cart_count(request.user),
        'wishlist_count': _wishlist_count(request.user),
        'order_count':    _order_count(request.user),
    }
    return render(request, 'store/user_home.html', context)


# ─────────────────────────────────────────
#  ADD TO CART
# ─────────────────────────────────────────
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get or create the cart item; increment if already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'"{product.name}" quantity updated in cart.')
    else:
        messages.success(request, f'"{product.name}" added to cart!')

    # Redirect back to wherever the user came from
    return redirect(request.META.get('HTTP_REFERER', 'user_home'))


# ─────────────────────────────────────────
#  REMOVE FROM CART
# ─────────────────────────────────────────
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect(request.META.get('HTTP_REFERER', 'user_home'))


# ─────────────────────────────────────────
#  ADD / TOGGLE WISHLIST
# ─────────────────────────────────────────
@login_required(login_url='login')
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    existing = Wishlist.objects.filter(user=request.user, product=product).first()
    if existing:
        existing.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'"{product.name}" added to wishlist!')

    return redirect(request.META.get('HTTP_REFERER', 'user_home'))