from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# User Agent identifica o navegador que está fazendo a requisição(sem isso pode retornar página vazia/erro, versão diferente ou bloqueia o site)
# Accept-Language diz quais idiomas você prefere receber, em ordem de prioridade
# Accept define quais tipos de conteúdo você aceita como resposta
# Connection mantém a conexão TCP aberta para possíveis próximas requisições (reuso de conexão). Pode melhorar performance em vários requests
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 OPR/127.0.0.0",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8", #
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",}

def get_next_page_url(soup: str, current_url: str):
    # procura o botão de "Próxima" paginação (o seletor pode variar)
    prox_link = soup.select_one("li.andes-pagination__button--next a") # encontre um <li> com a classe andes-pagination__button--next e dentro dele, encontre um <a> (link)
    if not prox_link:
        return None
    href = prox_link.get("href")
    if not href:
        return None
    return urljoin(current_url, href)


def scrape_mercadolivre(query: str, max_pages: int = 1):
    produto = query.strip().replace(" ", "-")
    base_url = f"https://lista.mercadolivre.com.br/{produto}_NoIndex_True"

    paginas_raspadas = 0
    # lista de produtos
    resultados = []

    # enquanto existir uma url e paginas_raspadas for menor que max_pages
    while base_url and paginas_raspadas < max_pages:
        # fazer requisição utilizando o headers (User Agent)
        r = requests.get(base_url, headers=headers, timeout=20, allow_redirects=True) # 20s (tempo máximo que o request vai esperar antes de desistir e dar erro)
                                                                                      # redirects permite que a requisição siga automaticamente para outra URL caso o servidor responda com um redirecionamento (HTTP 301/302/307/308), por exemplo quando a URL “genérica” é encaminhada para a URL “canônica” da busca.

        r.raise_for_status() # reporta o erro

        # URL final (caso tenha redirecionado pra /games/.../ps5...)
        final_url = r.url

        site = BeautifulSoup(r.text, "html.parser") # servidor manda dados como bytes e r.text retona o conteúdo convertido para string
                                                    # parser transforma o HTML em uma estrutura de tags navegável (find, find_all, etc)

        # Encontrar resultados
        titulos = site.find_all('h3', class_='poly-component__title-wrapper')
        precos = site.find_all('span', class_='andes-money-amount__fraction')
        links = site.find_all('a', class_='poly-component__title')
        imagens = site.find_all('img', class_='poly-component__picture')

        #Se acabar os resultados, stop
        if not titulos:
            break

        for titulo, preco, link, imagem in zip(titulos, precos, links, imagens): #zip junta várias sequências em paralelo, alinhadas por posição (Ex: [titulos1, titulos2];[precos1, precos2] -> [titulos1 precos1], [titulos2, precos2])
            titulos = titulo.get_text(strip=True)

            precos = preco.get_text(strip=True)
            #Transforma str em int e tira o separador "." (ex: "3.999" -> "3999")
            preco_int = int(precos.replace(".", ""))

            href = link.get("href")
            #Garante URL absoluta. urljoin junta as urls
            produto_url = urljoin("https://lista.mercadolivre.com.br", href)

            #Imagem pode vir em src ou data-src dependendo do caso
            imagem_url = imagem.get("src") or imagem.get("data-src") or ""

            resultados.append({
                "fonte": "mercadolivre",
                "query": query,
                "titulo": titulos,
                "preco": preco_int,       #Por enquanto inteiro (reais sem centavos)
                "produto_url": produto_url,
                "imagem_url": imagem_url,
            })

        #Conta páginas raspadas
        paginas_raspadas += 1
        #Pega a URL da próxima página para raspar
        base_url = get_next_page_url(site, final_url)

    return resultados

if __name__ == "__main__":
    produto = input("Digite o produto: ")
    itens = scrape_mercadolivre(produto, max_pages=1)

    for i, item in enumerate(itens, start=1):
        print(f"\n=== Produto {i} ===")
        print(f"Título: {item['titulo']}")
        print(f"Preço: R$ {item['preco']}")
        print(f"URL:   {item['produto_url']}")
        print(f"Img:   {item['imagem_url']}")