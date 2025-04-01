import requests
from bs4 import BeautifulSoup
import zipfile
import os

def download_ans_files():
    """
    Faz o download dos arquivos PDF do site da ANS
    """
    # URL base do site
    base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    # Criar diretório para os arquivos se não existir
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Fazer a requisição para a página
    response = requests.get(base_url)
    response.raise_for_status()
    
    # Parsear o HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lista para armazenar os nomes dos arquivos baixados
    downloaded_files = []
    
    # Procurar por links que contenham "Anexo I" ou "Anexo II" e que terminem em .pdf
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href and href.lower().endswith('.pdf'):
            if 'Anexo I' in link.text or 'Anexo II' in link.text:
                full_url = base_url + href if href.startswith('/') else href
                filename = os.path.join('downloads', f"{link.text.strip()}.pdf")
                download_file(full_url, filename)
                downloaded_files.append(filename)
    
    # Criar arquivo ZIP com os PDFs
    if downloaded_files:
        zip_filename = 'downloads/anexos_ans.zip'
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in downloaded_files:
                zipf.write(file, os.path.basename(file))
        print(f"\nArquivo ZIP '{zip_filename}' criado com sucesso!")
        
        # Remover os arquivos PDF individuais após criar o ZIP
        for file in downloaded_files:
            os.remove(file)
        print("Arquivos PDF individuais removidos.")
        
        return zip_filename
    else:
        raise Exception("Nenhum arquivo PDF encontrado para download")

def download_file(url, filename):
    """
    Faz o download de um arquivo da URL especificada
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Arquivo {filename} baixado com sucesso!") 