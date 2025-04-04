import os
import sys
import logging
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Testa a conexão com o banco de dados."""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Testa se as tabelas existem
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        
        logger.info("Tabelas encontradas no banco de dados:")
        for table in tables:
            logger.info(f"- {table[0]}")
            
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        return False

def test_data_files():
    """Verifica se os arquivos de dados necessários existem."""
    required_dirs = [
        'db/datas/demo-contabeis/2024',
        'db/datas/relatorio-operadoras'
    ]
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            logger.error(f"Diretório não encontrado: {dir_path}")
            return False
            
    return True

def main():
    """Executa todos os testes de configuração."""
    logger.info("Iniciando testes de configuração...")
    
    # Testa conexão com o banco
    if not test_database_connection():
        logger.error("❌ Falha no teste de conexão com o banco de dados")
        sys.exit(1)
    logger.info("✅ Conexão com o banco de dados OK")
    
    # Testa arquivos de dados
    if not test_data_files():
        logger.error("❌ Falha no teste de arquivos de dados")
        sys.exit(1)
    logger.info("✅ Arquivos de dados OK")
    
    logger.info("✅ Todos os testes passaram com sucesso!")

if __name__ == "__main__":
    main() 