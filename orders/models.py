from django.db import models
from products.models import Product


class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    payment_status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return (
            f"Order: {self.name} | {self.total_price} | {self.payment_status}"
        )
