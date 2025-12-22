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
from rest_framework.renderers import TemplateHTMLRenderer


class ScrapeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'scrape.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        search_term = request.data.get('search_term')
        
        if not search_term:
            return Response(
                {"erro": "Por favor, digite um termo de busca."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
        # Dispara o Celery
        task_execute_scraper.delay(search_term)
        
        # Retorna o template com mensagem de sucesso
        return Response({
            "message": f"Robô iniciado para o termo: '{search_term}'",
            "status": "Processando"
        }, status=status.HTTP_202_ACCEPTED)


class ProductsView(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products.html'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response({'products': response.data})

