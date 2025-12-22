from .models import Product
from django.db import transaction, IntegrityError

class ProductRepository():

    def create_many_products(products):
        
        product_instances = [
            Product(**product_data)
            for product_data in products
        ]
        try:
            with transaction.atomic():
                Product.objects.bulk_create(
                product_instances
            )
            return 
        except Exception as e:
            print(e)
            raise IntegrityError 