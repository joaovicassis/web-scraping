import os
import sys
from src.crawler import download_ans_files
from src.processor import process_pdf_data

def main():
    try:
        print("Iniciando processo de coleta e processamento de dados...")
        

        print("\n1. Fazendo download dos arquivos PDF...")
        pdf_zip_path = download_ans_files()
        

        print("\n2. Processando dados do PDF...")
        final_zip_path = process_pdf_data(pdf_zip_path)
        
        print("\nProcesso concluído com sucesso!")
        print(f"Arquivo final gerado: {final_zip_path}")
        
    except Exception as e:
        print(f"\nErro durante o processamento: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 