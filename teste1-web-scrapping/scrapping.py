import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

# URL da página da ANS
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Diretório para salvar os PDFs
output_dir = "anexos"
os.makedirs(output_dir, exist_ok=True)

# Requisição para obter o conteúdo da página
response = requests.get(url)
response.raise_for_status() # lançar erro caso falhe

# Parse do HTML
soup = BeautifulSoup(response.text, "html.parser") 

# Lista para armazenar os links dos PDFs
pdf_links = []
for link in soup.find_all("a", href=True):
    href = link["href"]
    if ("Anexo_I" in href or "Anexo_II" in href) and href.endswith(".pdf"):  # Garante que é um PDF
        if href.startswith("/"):  # Ajusta URLs relativas
            href = "https://www.gov.br" + href
        pdf_links.append(href)

# Baixando os PDFs
pdf_files = []
for pdf_url in pdf_links:
    pdf_name = pdf_url.split("/")[-1]
    pdf_path = os.path.join(output_dir, pdf_name)

    response = requests.get(pdf_url)
    with open(pdf_path, "wb") as f:
        f.write(response.content)

    pdf_files.append(pdf_path)
    print(f"Baixado: {pdf_name}")

# Compactação dos PDFs em um ZIP
zip_path = "anexos.zip"
with ZipFile(zip_path, "w") as zipf:
    for file in pdf_files:
        zipf.write(file, os.path.basename(file))

print(f"Arquivo ZIP criado: {zip_path}")
