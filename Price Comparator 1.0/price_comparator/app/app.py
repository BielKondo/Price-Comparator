from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.db import init_db
from app.api.routes.endpointsProd import router as products_router

# FastAPI transforma a função (async generator) em um objeto especial que controla início e fim do app.
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # Inicia o DataBase
    yield

# @app.on_event("startup")
# def startup():

# Utiliza lifespan para dizer “use essa função para startup/shutdown”
app = FastAPI(title="ML Scraper Tracker", lifespan=lifespan) 

# Registra todas as rotas definidas em app/api/products.py
app.include_router(products_router)

# Verifica se o servidor está ativo
@app.get("/")
def home(): 
    return {
        "status": "ok",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": ["/scrape (POST)", "/products (GET)", "/export (GET)"]
    }