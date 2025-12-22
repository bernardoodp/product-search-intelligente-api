from celery import shared_task
# Importe seu scraper original e o repositório
from api.scrapers.magalu import scrape_magalu 
from api.repository import ProductRepository

@shared_task
def task_execute_scraper(search_term):
    print(f"[WORKER] Iniciando busca por: {search_term}")
    
    try:
        produtos = scrape_magalu(search_term)
        
        if produtos:
            ProductRepository.create_many_products(produtos)
            return f"Sucesso! {len(produtos)} produtos salvos."
        
        return "Nenhum produto encontrado."

    except Exception as e:
        return f"Erro no scraper: {str(e)}"