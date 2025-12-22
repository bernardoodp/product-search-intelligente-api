# restframework 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import rest_framework.mixins as mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from api.tasks import task_execute_scraper


class ScrapeView(APIView):
    def post(self, request):
        search_term = request.data.get('search_term')
        
        if not search_term:
            return Response({"erro": "Termo de busca obrigatório"}, status=400)
    
        task_execute_scraper.delay(search_term)
        
        return Response({
            "message": "Robô iniciado em segundo plano!",
            "status": "Processando"
        }, status=status.HTTP_202_ACCEPTED)


class ProductsView(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

