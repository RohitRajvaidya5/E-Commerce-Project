from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
