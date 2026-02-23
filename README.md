# ML Scraper Tracker

API desenvolvida com FastAPI + SQLite + Pandas para realizar scraping de produtos do Mercado Livre, armazenar os dados em banco de dados relacional e gerar relatórios em Excel para análise posterior (ex: Power BI).

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:
* Praticar arquitetura backend organizada.
* Trabalhar com Web Scraping real.
* Persistir dados em banco relacional (SQLite).
* Criar uma API REST profissional com FastAPI.
* Gerar arquivos estruturados para análise no Power BI.
* Demonstrar conhecimento prático para portfólio.

**O sistema permite:**
* 🔎 Buscar produtos por palavra-chave.
* 💾 Armazenar os resultados no banco.
* 📊 Exportar os dados para Excel.
* 📈 Gerar abas analíticas automaticamente.

---

## 🏗️ Arquitetura do Projeto

```text
app/
 ├── api/
 │   └── routes/
 │       └── endpointsProd.py   # Endpoints da API
 ├── db/
 │   └── db.py                  # Conexão e queries SQLite
 ├── schemas/
 │   └── models.py              # Modelos Pydantic
 ├── services/
 │   ├── web_scraper.py         # Lógica de scraping
 │   └── export.py              # Geração de Excel
 └── app.py                     # Inicialização da aplicação
```

### Separação de Responsabilidades:

* **API**: Expor endpoints REST.
* **Services**: Regras de negócio (scraping e exportação).
* **DB**: Persistência e queries SQL.
* **Schemas**: Validação de dados com Pydantic.
* **App**: Inicialização e configuração do servidor.

---

## 🧠 Tecnologias Utilizadas

### 🚀 Backend
* **FastAPI**: Framework ASGI moderno e performático.
* **Pydantic**: Validação de dados e schemas.
* **SQLite**: Banco de dados leve e integrado.
* **Uvicorn**: Servidor ASGI para rodar a aplicação.

### 🕸️ Web Scraping
* **Requests**: Realização de requisições HTTP.
* **BeautifulSoup (bs4)**: Parsing e extração de dados do HTML.

### 📊 Análise e Exportação
* **Pandas**: Manipulação e tratamento de dados.
* **OpenPyXL**: Engine para escrita de arquivos Excel (.xlsx).

---

## 🗄️ Estrutura do Banco de Dados (Tabela: products)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| id | INTEGER | Chave Primária (Auto-incremento) |
| query | TEXT | Termo utilizado na busca |
| posicao | INTEGER | Posição no ranking do ML |
| titulo | TEXT | Nome do produto |
| preco | INTEGER | Valor numérico limpo |
| produto_url | TEXT | Link direto da oferta |
| imagem_url | TEXT | Link da imagem miniatura |
| captured_at | DATETIME | Data e hora da extração |

---

## 🔌 Endpoints da API

Documentação interativa disponível em: `http://127.0.0.1:8000/docs`

* **POST /scrape**: Inicia a extração. Parâmetros: `q` (termo) e `pages` (qtd).
* **GET /products**: Retorna os itens do banco. Suporta filtros e limite.
* **GET /export**: Gera e baixa o relatório analítico em Excel.

---

## 📊 Relatório Excel Automatizado

O arquivo gerado pelo endpoint `/export` contém:
1. **Dados Brutos**: Tabela completa com todos os itens capturados.
2. **Top 20 Baratos**: Filtro automático dos melhores preços.
3. **Resumo Analítico**: Estatísticas de Preço Médio, Mínimo e Máximo por busca.

---

## ⚙️ Como Executar o Projeto

**1. Clonar repositório:**
`git clone https://github.com/seu-usuario/ml-scraper-tracker.git`

**2. Criar ambiente virtual:**
`python -m venv .venv`

**3. Ativar ambiente:**
* Windows: `.\.venv\Scripts\activate`
* Linux/Mac: `source .venv/bin/activate`

**4. Instalar dependências e rodar:**
`pip install -r requirements.txt`
`uvicorn app.app:app --reload`

---

## 📌 Notas Importantes
> Este projeto possui fins estritamente educacionais. O funcionamento do scraper depende da estrutura
