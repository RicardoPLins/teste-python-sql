from fastapi import FastAPI, Query
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permite requisições do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# Carrega os dados do CSV na inicialização do servidor
CSV_FILE = r'..\Relatorio_cadop.csv'  # Caminho do csv de operadoras
df = pd.read_csv(CSV_FILE, delimiter=';', encoding='utf8')

@app.get("/operadoras")
def list_operadoras():
    """Retorna todas as operadoras do arquivo CSV, lidando com NaN e valores inválidos."""
    return df.fillna("").to_dict(orient="records")

@app.get("/search")
def search_operadoras(query: str = Query(..., description="Texto para buscar operadoras")):
    """Busca operadoras pelo nome social ou nome fantasia."""
    results = df[
        df['Razao_Social'].str.contains(query, case=False, na=False) |
        df['Nome_Fantasia'].str.contains(query, case=False, na=False)
    ]
    
    return results.fillna("").head(10).to_dict(orient="records")


# para rodar o server: python -m uvicorn server:app --reload