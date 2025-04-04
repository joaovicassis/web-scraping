import os
import psycopg2
from psycopg2 import sql
from typing import Optional
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or os.getenv('DATABASE_URL')
        if not self.db_url:
            raise ValueError("URL do banco de dados não fornecida. Configure a variável de ambiente DATABASE_URL.")
        
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cur = self.conn.cursor()
            logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            logger.info("Conexão com o banco de dados fechada.")

    def execute_sql_file(self, file_path: str):
        """
        Executa um arquivo SQL.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_commands = f.read()
            
            logger.info(f"Executando arquivo SQL: {file_path}")
            self.cur.execute(sql_commands)
            self.conn.commit()
            logger.info("Comandos SQL executados com sucesso.")
            
        except Exception as e:
            logger.error(f"Erro ao executar arquivo SQL {file_path}: {str(e)}")
            self.conn.rollback()
            raise

    def setup_database(self):
        """Executa todos os scripts SQL na ordem correta."""
        try:
            self.connect()
            
            base_dir = Path(__file__).parent.parent / 'sql'
            
            scripts = [
                base_dir / 'schema' / 'create_tables.sql',
                base_dir / 'import' / 'import_data.sql',
                base_dir / 'cleanup' / 'cleanup_data.sql',
                base_dir / 'verify' / 'verify_data.sql'
            ]
            
            for script in scripts:
                if script.exists():
                    self.execute_sql_file(str(script))
                else:
                    logger.warning(f"Arquivo SQL não encontrado: {script}")
            
        except Exception as e:
            logger.error(f"Erro durante a configuração do banco de dados: {str(e)}")
            raise
        finally:
            self.disconnect()

def main():
    try:
        db_manager = DatabaseManager()
        db_manager.setup_database()
        logger.info("Configuração do banco de dados concluída com sucesso.")
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main() 