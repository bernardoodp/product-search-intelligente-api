# api/services.py
from .repository import ProductRepository
from .scrapers.magalu import scrape_magalu
class ProductSearchService:
    def search_and_save(self, term):
        # 1. Chama o Scraper
        data = scrape_magalu(term)
        
        # 2. Validações de negócio
        if not isinstance(data, list):
            raise Exception(f"Erro no scraper: {data}")
            
        # 3. Chama o Repositório
        ProductRepository.create_many_products(data)
        return data