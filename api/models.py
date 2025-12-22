from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.TextField()
    price = models.IntegerField()
    image_url = models.TextField()
    product_url = models.TextField()
    site_url = models.TextField()

    def __str__(self):
        return self.name
