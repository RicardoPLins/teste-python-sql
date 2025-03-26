import os
import pdfplumber
import pandas as pd
from zipfile import ZipFile

# Caminho do PDF baixado no teste 1
pdf_file = os.path.join("..", "web-scrapping", "anexos", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
csv_file = "Teste_Ricardo_Lins.csv"  # Nome do arquivo CSV
zip_file = "Teste_Ricardo_Lins.zip"  # Nome do ZIP

# Dicionário de substituição das abreviações OD e AMB
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}

# Lista para armazenar os dados extraídos
dados_extraidos = []

# Abre o PDF e extrai as tabelas de todas as páginas
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table:
                if any(row):  # Verifica se a linha não está vazia
                    dados_extraidos.append([cell.strip() if cell else "" for cell in row])  # Remove espaços extras

# Verifica se há dados extraídos
if dados_extraidos:
    # Convertendo os dados extraídos em um DataFrame
    df = pd.DataFrame(dados_extraidos)

    # 🔹 **Correção do cabeçalho**
    df.columns = df.iloc[0].astype(str).str.replace(r'\n', ' ', regex=True).str.strip()  # Remove quebras de linha e espaços extras
    df = df[1:].reset_index(drop=True)  # Remove a linha duplicada do cabeçalho

    # 🔹 **Aplicar substituição nas colunas e no conteúdo**
    df.columns = [substituicoes.get(col.strip(), col.strip()) for col in df.columns]  # Substituir OD e AMB no cabeçalho
    df.replace(substituicoes, inplace=True)  # Substituir OD e AMB no conteúdo

    # Salvar o DataFrame como CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")

    # Compactar o CSV em um arquivo ZIP
    with ZipFile(zip_file, "w") as zipf:
        zipf.write(csv_file)

    print(f"Arquivo ZIP criado: {zip_file}")
else:
    print("Nenhuma tabela encontrada no PDF. Verifique o arquivo.")
