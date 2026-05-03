from django.db import models
from django.conf import settings  # ✅ always use this when your project has a custom User model


# ─────────────────────────────────────────
#  PRODUCT
# ─────────────────────────────────────────
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Laptop',      'Laptop'),
        ('Accessories', 'Accessories'),
        ('Mobile',      'Mobile'),
        ('Other',       'Other'),
    ]
    name        = models.CharField(max_length=100)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category    = models.CharField(
                      max_length=50,
                      choices=CATEGORY_CHOICES,
                      default='Other'
                  )
    image       = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


# ─────────────────────────────────────────
#  CART  (one per user)
# ─────────────────────────────────────────
class Cart(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())


# ─────────────────────────────────────────
#  CART ITEM
# ─────────────────────────────────────────
class CartItem(models.Model):
    cart     = models.ForeignKey(Cart,    on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    def subtotal(self):
        return self.product.price * self.quantity


# ─────────────────────────────────────────
#  WISHLIST
# ─────────────────────────────────────────
class Wishlist(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')   # no duplicates

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"