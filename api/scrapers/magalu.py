from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import re
from decimal import Decimal

def scrape_magalu(search_term):
    print(f"Starting scraping for: {search_term}...")

    site_url = "https://www.magazineluiza.com.br"
    with Stealth().use_sync(sync_playwright()) as p:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        
        context = browser.new_context(
            user_agent=user_agent,
            locale='pt-BR',
            timezone_id='America/Sao_Paulo'
        )
        
        page = context.new_page()
    

        try:
            page.goto(f"{site_url}/busca/{search_term}/", timeout=60000, wait_until="domcontentloaded")
        
            page.wait_for_selector('[data-testid="product-card-container"]', timeout=30000)
            
            print("Products found. Extracting data...")
            produtos_html = page.query_selector_all('[data-testid="product-card-container"]')
            
            products = []

            print(f"Encontrados {len(produtos_html)} cards. Processando os 10 primeiros...")
            for i, product in enumerate(produtos_html):
                if i >= 10:
                    break
                try:
                    title_element = product.query_selector('[data-testid="product-title"]')
                    title = title_element.inner_text() if title_element else "Sem Título"

                    price_element = product.query_selector('[data-testid="price-value"]')
                    price = price_element.inner_text() if price_element else "Sem Preço"
                    formatted_price = int(
                        Decimal(
                            re.sub(r"[^\d,]", "", price).replace(",", ".")
                        ) * 100
                    )
                    
                    link_element = product.get_attribute('href')

                    link_image_element = product.query_selector('[data-testid="image"]')
                    image = link_image_element.get_attribute('src')
                    
                    if not link_element:
                        link_element = product.query_selector('a')
                    
                    link = link_element
                    if link:
                        if not link.startswith('http'):
                            link = site_url + link
                    else:
                        link = "Link não encontrado"

                    products.append({
                        "name": title,
                        "price": formatted_price,
                        "product_url": link,
                        "image_url": image,
                        "site_url": site_url

                    })
                except Exception as e:
                    print(f"Erro ao ler item {i}: {e}")
            
            browser.close()
            return products

        except Exception as e:
            print(f"Erro durante o scraping: {e}")
            page.screenshot(path="/app/erro_bloqueio.png")
            browser.close()
            raise Exception("Falha no scraping ou bloqueio detectado")