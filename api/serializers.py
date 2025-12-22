from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = "__all__"
        model = Product

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        data['price'] = instance.price / 100
        
        return data