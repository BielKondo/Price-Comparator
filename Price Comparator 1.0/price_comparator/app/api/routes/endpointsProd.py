from typing import Optional, List
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from pathlib import Path
from db.db import insert_products, list_products
from services.web_scraper import scrape_mercadolivre
from services.export import export_to_excel
from schemas.models import ProductOut

router = APIRouter(tags=["products"])  # Endpoints aparecem organizado no /docs por "products"

# Faz scraping no Mercado Livre e salva no SQLite
@router.post("/scrape")
def scrape_and_store(
    q: str = Query(..., min_length=1), # "..." significa obrigatório e min_length impede str vazia
    pages: int = Query(1, ge=1, le=10), # >= 1 e <= 10
):
    rows = scrape_mercadolivre(q, max_pages=pages)
    inserted = insert_products(rows)
    return {
        "query": q,
        "scraped": f"{len(rows)} rows",
        "inserted": f"{inserted} rows",
    }

# Lista produtos salvos no banco
@router.get("/products", response_model=List[ProductOut])
def get_products(
    q: Optional[str] = None,
    limit: int = Query(200, ge=1, le=2000), # padrão 200, >= 1 e <= 2000 resultados
):
    return list_products(query=q, limit=limit)

# Gera um Excel e devolve para download
@router.get("/export")
def export_products(
    q: Optional[str] = None,
    limit: int = Query(2000, ge=1, le=20000),
):
    rows = list_products(query=q, limit=limit)
    path = export_to_excel(rows)

    # retorna o arquivo para download
    return FileResponse(
        path=path,
        filename=Path(path).name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", # Informa ao navegador que é um arquivo Excel .xlsx e ele trata como download corretamente.
    )