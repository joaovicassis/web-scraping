import pdfplumber
import pandas as pd
import zipfile
import os
import shutil

def process_pdf_data(pdf_zip_path):
    if not os.path.exists(pdf_zip_path):
        raise Exception(f"Arquivo ZIP não encontrado em: {pdf_zip_path}")
    

    temp_dir = "temp_pdf"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    with zipfile.ZipFile(pdf_zip_path, 'r') as zip_ref:
        anexo_encontrado = False
        for file in zip_ref.namelist():
            if "Anexo I" in file:
                zip_ref.extract(file, temp_dir)
                pdf_file = os.path.join(temp_dir, file)
                anexo_encontrado = True
                break
        
        if not anexo_encontrado:
            raise Exception("Anexo I não encontrado no arquivo ZIP")
        
    print("Extraindo tabelas do PDF...")
    all_tables = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processando página {page_num}...")
                page_tables = page.extract_tables()
                if page_tables and len(page_tables) > 0:
                    table = page_tables[0]
                    if table and len(table) > 0:
                        if page_num == 1:
                            all_tables.append(table)
                        else:
                            all_tables.append(table[1:])
    except Exception as e:
        print(f"Erro ao extrair tabelas: {str(e)}")
        raise
    
    if not all_tables:
        raise Exception("Nenhuma tabela encontrada no PDF")
    

    print("Combinando dados de todas as páginas...")
    combined_data = []
    headers = all_tables[0][0] 
    
    for table in all_tables:
        if len(table) > 1: 
            combined_data.extend(table[1:])
    
    target_table = pd.DataFrame(combined_data, columns=headers)
    
    target_table = target_table.fillna('')  # Substituir valores NaN por string vazia
    
    target_table = target_table.rename(columns={
        'OD': 'Seg. Odontológica',
        'AMD': 'Seg. Ambulatorial'
    })
    
    if not os.path.exists('processed_data'):
        os.makedirs('processed_data')
    
    csv_path = 'processed_data/rol_procedimentos.csv'
    try:
        target_table.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"\nCSV salvo com sucesso em: {csv_path}")
        print(f"Total de linhas processadas: {len(target_table)}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {str(e)}")
        raise
    
    zip_path = 'Teste_Joao_Assis.zip'
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"Arquivo ZIP '{zip_path}' criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar arquivo ZIP: {str(e)}")
        raise
    
    try:
        shutil.rmtree(temp_dir)
        os.remove(csv_path)
        print("Arquivos temporários removidos.")
    except Exception as e:
        print(f"Aviso: Não foi possível remover alguns arquivos temporários: {str(e)}")
        
    return zip_path 