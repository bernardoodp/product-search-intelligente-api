from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    image_url = models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)
    site_url = models.CharField(max_length=255)

