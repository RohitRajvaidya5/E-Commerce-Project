from django.db import models
from products.models import Product


class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Order : {self.id}"

