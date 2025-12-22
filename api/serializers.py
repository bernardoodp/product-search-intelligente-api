from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = "__all__"
        model = Product

    def to_representation(self, instance):
        # Pega a representação original (o dicionário com os dados)
        data = super().to_representation(instance)
        
        # Altera o preço dividindo por 100
        data['price'] = instance.price / 100
        
        return data