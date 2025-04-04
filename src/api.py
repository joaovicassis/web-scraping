from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Busca de Operadoras",
    description="API para busca textual em cadastros de operadoras de saúde",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """Estabelece conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados")

@app.get("/")
async def root():
    """Rota raiz da API."""
    return {
        "message": "API de Busca de Operadoras",
        "version": "1.0.0",
        "endpoints": {
            "/search": "Busca textual em operadoras",
            "/health": "Verificação de saúde da API"
        }
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API."""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/search", response_model=List[dict])
async def search_operadoras(
    query: str = Query(..., description="Termo de busca"),
    limit: int = Query(10, description="Número máximo de resultados"),
    offset: int = Query(0, description="Número de resultados para pular"),
    uf: Optional[str] = Query(None, description="Filtrar por UF"),
    modalidade: Optional[str] = Query(None, description="Filtrar por modalidade")
):
    """
    Realiza busca textual em operadoras.
    
    A busca é feita nos campos:
    - registro_ans
    - razao_social
    - nome_fantasia
    - cidade
    - bairro
    
    Os resultados são ordenados por relevância.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Construção da query base
        base_query = """
            SELECT 
                registro_ans,
                cnpj,
                razao_social,
                nome_fantasia,
                modalidade,
                cidade,
                uf,
                bairro
            FROM relatorio_operadoras
            WHERE 
                (
                    registro_ans ILIKE %s OR
                    razao_social ILIKE %s OR
                    nome_fantasia ILIKE %s OR
                    cidade ILIKE %s OR
                    bairro ILIKE %s
                )
        """
        
        # Parâmetros da busca
        search_term = f"%{query}%"
        params = [search_term] * 5
        
        # Adiciona filtros opcionais
        if uf:
            base_query += " AND uf = %s"
            params.append(uf.upper())
        
        if modalidade:
            base_query += " AND modalidade = %s"
            params.append(modalidade)
        
        base_query += """
            ORDER BY 
                CASE 
                    WHEN razao_social ILIKE %s THEN 1
                    WHEN nome_fantasia ILIKE %s THEN 2
                    ELSE 3
                END,
                razao_social
            LIMIT %s OFFSET %s
        """
        
        params.extend([search_term, search_term, limit, offset])
        
        cur.execute(base_query, params)
        results = cur.fetchall()
        
        return [dict(row) for row in results]
        
    except Exception as e:
        logger.error(f"Erro durante a busca: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 