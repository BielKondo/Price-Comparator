import pandas as pd # Manipulação de dados
from datetime import datetime
from typing import List, Dict, Any 
from pathlib import Path

def export_to_excel(rows: List[Dict[str, Any]], out_path: str | None = None) -> str: # out_path nome ou caminho do arquivo de saída
    if not rows:
        raise ValueError("Sem dados para exportar.")

    df = pd.DataFrame(rows) # Converte a lista de dicionários para um DataFrame do pandas (tabela)

    # Se "c" estiver em df.columns, seráa dicionado a cols
    cols = [c for c in ["id","query","posicao","titulo","preco","produto_url","imagem_url","captured_at"] if c in df.columns]
    # DataFrame terá as colnuas que foram verificadas anteriormente e na ordem em que estão
    df = df[cols] if cols else df # Se não houver "cols", df = df

    # Nome padrão com timestamp (ts)
    if not out_path: 
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"ml_export_{ts}.xlsx"

    # Transforma out_path em um objeto Path chamado out (funções: .parent [pasta], .name, .exists, .resolve [caminho absoluto])
    out = Path(out_path) 

    # Abas úteis pro Power BI
    #ExcelWriter cria várias abas no mesmo arquivo (evita o risco de sobrescrever)

    # out é o destino do arquivo
    # engine="openpyxl" é a biblioteca que o pandas vai usar para escrever um .xlsx
    with pd.ExcelWriter(out, engine="openpyxl") as writer: 
        df.to_excel(writer, sheet_name="Dados", index=False)

        if "preco" in df.columns:
            # Ordena em ordem crescente
            df_sorted = df.sort_values("preco", ascending=True)
            # Pega os 20 mais baratos
            df_sorted.head(20).to_excel(writer, sheet_name="Top_20_Mais_Baratos", index=False)

        if "query" in df.columns:
            #as_index=False mantém "query" como coluna normal, e não como índice
            resumo = df.groupby("query", as_index=False).agg(   #agg agrega colunas por grupo
                itens=("titulo", "count"),
                preco_min=("preco", "min"),
                preco_med=("preco", "median"),
                preco_max=("preco", "max"),
            )
            resumo.to_excel(writer, sheet_name="Resumo_por_Query", index=False)

    return str(out)