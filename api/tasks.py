from celery import shared_task
from api.scrapers.magalu import scrape_magalu 
from api.scrapers.mercado_livre import scrape_mercado_livre
from api.repository import ProductRepository

@shared_task
def task_execute_scraper(search_term):
    print(f"[WORKER] Iniciando busca por: {search_term}")
    
    all_products = []
    erros = []

    try:
        print("Buscando no Magalu...")
        magalu_products = scrape_magalu(search_term)
        all_products.extend(magalu_products)
        print(f"Magalu retornou {len(magalu_products)} itens.")
    except Exception as e:
        print(f"Erro ao buscar no Magalu: {e}")
        erros.append("Magalu falhou")

    try:
        print("Buscando no Mercado Livre...")
        ml_products = scrape_mercado_livre(search_term)
        all_products.extend(ml_products)
        print(f"Mercado Livre retornou {len(ml_products)} itens.")
    except Exception as e:
        print(f"Erro ao buscar no Mercado Livre: {e}")
        erros.append("ML falhou")
    if all_products:
        all_products.sort(key=lambda x: x['price'])
        
        ProductRepository.create_many_products(all_products)
        
        msg = f"Sucesso! {len(all_products)} produtos salvos."
        
        if erros:
            msg += f" (Atenção: {', '.join(erros)})"
            
        return msg
    
    return "Nenhum produto encontrado em nenhuma das lojas."