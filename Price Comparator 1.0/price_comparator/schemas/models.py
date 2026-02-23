from pydantic import BaseModel #Classe base para criar modelos de dados
from typing import Optional #Tipo opcional para as variáveis
from datetime import datetime #Tipo data e hora

# Padronização de dados
# Pydantic valida campos faltando, tipos errados, etc. Isso facilita a manutenção (erros claros) e a escalabilidade do código. Se houver endpoints (pontos de acesso da minha API), este arquivo vira o "schema" (estrutura de dados que um objeto deve seguir)

# Modelo de entrada para os produtos
class ProductIn(BaseModel):
    query: str
    posicao: int
    titulo: str
    preco: int
    produto_url: str
    imagem_url: Optional[str] = ""

# Modelo de saída para os produtos 
class ProductOut(ProductIn): 
    id: int
    captured_at: datetime

class ScrapeResult(BaseModel):
    query: str
    scraped: int
    inserted: int