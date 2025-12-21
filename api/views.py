from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from scrapers.magalu import scrape_magalu

class ProductsView(APIView):

    def post(self, request):
        data = request.data
        search_term = data.get('search_term', None)
        if not search_term:
            return Response({"detail": "Search term é necessário para ser feito o POST"})
        
        products_from_magalu = scrape_magalu(search_term)

