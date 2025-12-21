from playwright.sync_api import sync_playwright
import re
from decimal import Decimal


def scrape_magalu(search_term=None):
    site_url = "https://www.magazineluiza.com.br"
    try: 
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                    headless=True,  
                    args=["--start-maximized"] 
                )
            
            context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080}
                )
            
            page = context.new_page()

            print("Acessando o site...")
            page.goto(f"{site_url}/busca/{search_term}/")

            try:
                page.wait_for_selector('[data-testid="product-card-container"]', timeout=15000)
            except Exception as e:
                print("Erro: O site demorou demais ou detectou o robô.")
                # Se cair aqui, tire um print para ver se apareceu captcha
                page.screenshot(path="erro_bloqueio.png")
                browser.close()
                raise Exception("Elemento não encontrado") 
            # 4. Pega os produtos usando seletores de teste (data-testid)
            # Esses atributos não mudam como as classes css (sc-xyz...)
            produtos_html = page.query_selector_all('[data-testid="product-card-container"]')
            
            collected_data = []

            print(f"Encontrados {len(produtos_html)} cards. Processando os 10 primeiros...")
            for i, product in enumerate(produtos_html):
                if i >= 10:
                    break
                try:
                    # 1. TÍTULO
                    title_element = product.query_selector('[data-testid="product-title"]')
                    title = title_element.inner_text() if title_element else "Sem Título"

                    # 2. PREÇO
                    price_element = product.query_selector('[data-testid="price-value"]')
                    price = price_element.inner_text() if price_element else "Sem Preço"
                    formatted_price = int(
                        Decimal(
                            re.sub(r"[^\d,]", "", price).replace(",", ".")
                        ) * 100
                    )
                    
                    # 3. LINK (Correção aqui)
                    # Estratégia A: Procura um link com o data-testid específico de conteúdo (padrão Magalu)
                    link_element = product.get_attribute('href')

                    link_image_element = product.query_selector('[data-testid="image"]')
                    image = link_image_element.get_attribute('src')
                    
                    # Estratégia B: Se não achar, procura qualquer tag 'a'
                    if not link_element:
                        link_element = product.query_selector('a')
                    
                    # Tratamento final da URL
                    link = link_element
                    if link:
                        if not link.startswith('http'):
                            link = site_url + link
                    else:
                        link = "Link não encontrado"

                    collected_data.append({
                        "name": title,
                        "price": formatted_price,
                        "product_url": link,
                        "image_url": image,
                        "site_url": site_url

                    })

                except Exception as e:
                    print(f"Erro ao ler item {i}: {e}")

            browser.close()
            return collected_data   
    except Exception as e:
        raise Exception("Elemento não encontrado")