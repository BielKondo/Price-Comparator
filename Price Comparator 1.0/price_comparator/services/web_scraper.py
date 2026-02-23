from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from typing import List, Dict, Any, Optional

# User Agent identifica o navegador que está fazendo a requisição(sem isso pode retornar página vazia/erro, versão diferente ou bloqueia o site)
# Accept-Language diz quais idiomas você prefere receber, em ordem de prioridade
# Accept define quais tipos de conteúdo você aceita como resposta
# Connection mantém a conexão TCP aberta para possíveis próximas requisições (reuso de conexão). Pode melhorar performance em vários requests
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 OPR/127.0.0.0",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8", #
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",}

def get_next_page_url(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    # procura o botão de "Próxima" paginação (o seletor pode variar)
    prox_link = soup.select_one("li.andes-pagination__button--next a") # encontre um <li> com a classe andes-pagination__button--next e dentro dele, encontre um <a> (link)
    if not prox_link:
        return None
    href = prox_link.get("href")
    if not href:
        return None
    return urljoin(current_url, href)


def scrape_mercadolivre(query: str, max_pages: int = 1) -> List[Dict[str, Any]]:
    #global url_ML
    produto = query.strip().replace(" ", "-")
    base_url = f"https://lista.mercadolivre.com.br/{produto}_NoIndex_True"

    paginas_raspadas = 0
    # Lista de produtos (dicionários com chaves e valores)
    resultados: List[Dict[str, Any]] = []

    # Enquanto existir uma url e paginas_raspadas for menor que max_pages
    while base_url and paginas_raspadas < max_pages:
        # Fazer requisição utilizando o headers (User Agent)
        r = requests.get(base_url, headers=headers, timeout=20, allow_redirects=True) # 20s (tempo máximo que o request vai esperar antes de desistir e dar erro)
                                                                                      # Redirects permite que a requisição siga automaticamente para outra URL caso o servidor responda com um redirecionamento (HTTP 301/302/307/308), por exemplo quando a URL “genérica” é encaminhada para a URL “canônica” da busca.

        r.raise_for_status() # Reporta o erro

        # URL final (caso tenha redirecionado pra /games/.../ps5...)
        final_url = r.url
        #url_ML = final_url

        site = BeautifulSoup(r.text, "html.parser") # Servidor manda dados como bytes e r.text retona o conteúdo convertido para string
                                                    # Parser transforma o HTML em uma estrutura de tags navegável (find, find_all, etc)

        # Lista principal de resultados (ol com as duas classes no MESMO elemento — ponto, sem espaço)
        lista_produtos = site.select_one("ol.ui-search-layout.ui-search-layout--grid")
        
        # Alternativas que o ML pode usar
        if not lista_produtos:
            # pega todos os poly-card (pode misturar patrocinados + lista e alterar ordem)
            produtos = site.select("div.poly-card")
            cards = [(i, card) for i, card in enumerate(produtos, start=1)]
        else:
            # Ordem estável: dentro do <ol>, pega as <li> na ordem do DOM (lista principal só)
            li_tag = lista_produtos.find_all("li", class_="ui-search-layout__item")
            cards = []
            for i, li in enumerate(li_tag, start=1):
                card = li.select_one("div.poly-card")
                if card:
                    cards.append((i, card))


        for pos, card in cards:
            # título
            titulos = card.select_one("h3.poly-component__title-wrapper")
            if not titulos:
                continue
            titulo = titulos.get_text(strip=True)

            # link (às vezes o título já é o <a>)
            links = card.select_one("h3.poly-component__title-wrapper a.poly-component__title")
            produto_url = links.get("href") if links else None
            if not produto_url:
                continue

            # imagem
            imgs = card.select_one("img.poly-component__picture")
            imagem_url = ""
            if imgs:
                imagem_url = imgs.get("src") or imgs.get("data-src") or ""

            # preço
            precos = card.select_one("div.poly-price__current span.andes-money-amount__fraction")
            if not precos:
                continue
            preco_txt = precos.get_text(strip=True)
            # transforma str em int e retira o ponto "3.789" -> 3789
            preco_int = int(preco_txt.replace(".", ""))

            resultados.append({
                "query": query,
                "posicao": pos,
                "titulo": titulo,
                "preco": preco_int,
                "produto_url": produto_url,
                "imagem_url": imagem_url,
            })

        

        #Conta páginas raspadas
        paginas_raspadas += 1
        #Pega a URL da próxima página para raspar
        base_url = get_next_page_url(site, final_url)

    return resultados
    