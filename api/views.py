from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
import rest_framework.mixins as mixins
from rest_framework.viewsets import GenericViewSet
from .services import ProductSearchService


class ScrapeView(APIView):
    def post(self, request):
        term = request.data.get('search_term')
        try:
            ProductSearchService().search_and_save(term)
            return Response({"detail": "Sucesso"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ProductsView(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

