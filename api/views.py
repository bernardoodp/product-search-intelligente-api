from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .scrapers.magalu import scrape_magalu
from .repository import ProductRepository
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer

class ProductsView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return super().get_queryset()
    
    def create(self, request, *args, **kwargs):
        
        data = request.data
        search_term = data.get('search_term', None)
        if not search_term:
            return Response({"detail": "Search term é necessário para ser feito o POST"})
        
        products_from_magalu = scrape_magalu(search_term)
        if not isinstance(products_from_magalu, list):
            return Response({"error": products_from_magalu}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            ProductRepository.create_many_products(products_from_magalu)
            return Response({"detail": "Produtos cadastrados com sucesso"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Erro ao cadastrar produtos: " + e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

