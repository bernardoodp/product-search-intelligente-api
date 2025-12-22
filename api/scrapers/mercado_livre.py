import requests
from bs4 import BeautifulSoup

def scrape_mercado_livre(search_term):
    term_formatted = search_term.replace(' ', '-')
    url = f"https://lista.mercadolivre.com.br/{term_formatted}"
    site_url = "https://www.mercadolivre.com.br"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, 'html.parser')

        products_html = soup.select('li.ui-search-layout__item')
        
        if not products_html:
            products_html = soup.select('div.ui-search-result__wrapper')

        print(f"Encontrados {len(products_html)} cards. Processando os 10 primeiros...")
        
        products = []

        for i, product in enumerate(products_html):
            if i >= 10:
                break
            
            try:
                title_element = product.select_one('h3.poly-component__title-wrapper, h2.ui-search-item__title')
                title = title_element.get_text(strip=True) if title_element else "Sem Título"

                price_element = product.select_one('.andes-money-amount__fraction')
                if price_element:
                    price_text = price_element.get_text(strip=True).replace('.', '')
                    price = int(price_text) * 100 
                else:
                    price = 0

                link_element = product.select_one('a.poly-component__title, a.ui-search-item__group__element')
                link = link_element['href'] if link_element else None

                img_element = product.select_one('img.poly-component__picture, img.ui-search-result-image__element')
                image = None
                if img_element:
                    image = img_element.get('data-src') or img_element.get('src')

                if link:
                    products.append({
                        "name": title,
                        "price": price,
                        "product_url": link,
                        "image_url": image,
                        "site_url": site_url
                    })

            except Exception as e:
                print(f"Erro ao ler item {i}: {e}")

        return products

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []