import sqlite3 # SQLite é um banco de dados leve e auto-contido que não requer servidor ou configuração complexa.
from pathlib import Path # Path é uma classe que representa caminhos de arquivos e diretórios.
from typing import Iterable, Optional, Dict, Any, List # Tipos para as variáveis

DB_PATH = Path("ml_tracker.sqlite3") # Caminho do banco de dados

def get_conn():
    conn = sqlite3.connect(DB_PATH) # Conecta ao banco de dados
    conn.row_factory = sqlite3.Row # Retorna os resultados como dicionários (chave : valor)
    return conn

def init_db(): # Inicializa o banco de dados
    with get_conn() as conn: # Conecta ao banco de dados (with garante que a conexão será fechada corretamente ao final) 
        conn.execute(""" 
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            posicao INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            preco INTEGER NOT NULL,
            produto_url TEXT NOT NULL,
            imagem_url TEXT,
            captured_at DATETIME DEFAULT (datetime('now'))
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_products_query_time ON products(query, captured_at);") # Índice para consultas rápidas por query e data de captura
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_products_url ON products(produto_url);") # Índice para consultas rápidas por URL do produto


def insert_products(rows: Iterable[Dict[str, Any]]) -> int: # Insere os produtos no banco de dados (rows é um iterável de dicionários) 
    rows = list(rows) # Converte o iterável para uma lista para verificar se está vazio e ser usado no executemany
    if not rows:
        return 0

    with get_conn() as conn:
        conn.executemany("""
            INSERT OR IGNORE INTO products (query, posicao, titulo, preco, produto_url, imagem_url)
            VALUES (:query, :posicao, :titulo, :preco, :produto_url, :imagem_url)
        """, rows) 
        # VALUES: Parâmetros nomeados: “Pegue o valor do parâmetro com esse nome e substitua na hora de executar.” (evita SQL injection)
        return len(rows) # Retorna o número de linhas inseridas

def list_products(query: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]: # Lista os produtos no banco de dados (query é opcional [pode ser str ou None], limit é o número de produtos a serem listados)
    with get_conn() as conn:
        if query: 
            cur = conn.execute("""
                SELECT * FROM products
                WHERE query = ? 
                ORDER BY captured_at DESC, posicao ASC
                LIMIT ?
            """, (query, limit)) # Parâmetros: query e limit
            # Ordena por data de captura decrescente e posição crescente
        else:
            cur = conn.execute("""
                SELECT * FROM products
                ORDER BY captured_at DESC, posicao ASC
                LIMIT ?
            """, (limit,))
        return [dict(r) for r in cur.fetchall()] # Converte os resultados para dicionários (chave : valor) [Fetchall() retorna uma lista de tuplas, e dict() converte cada tupla para um dicionário]