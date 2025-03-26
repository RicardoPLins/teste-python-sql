import pandas as pd
import os

# Diretório onde estão os arquivos CSV originais
directory = r'.\T2024' #ajustar para T2024 ou T2023

# Diretório de saída para os arquivos corrigidos
output_directory = r'C:\Program Files\PostgreSQL\16\data'

# Loop pelos trimestres de 1 a 4
for trimestre in range(1, 5):
    input_file = os.path.join(directory, f'{trimestre}T2024.csv') # ajustar os nomes aqui para 2023 ou 2024
    output_file = os.path.join(output_directory, f'{trimestre}T2024_corrigido.csv') # ajustar os nomes aqui para 2023 ou 2024
    
    try:
        # Carregar o arquivo CSV
        df = pd.read_csv(input_file, delimiter=';', encoding='UTF8')

        # Substituir as vírgulas por pontos nas colunas numéricas
        df['VL_SALDO_INICIAL'] = df['VL_SALDO_INICIAL'].replace({',': '.'}, regex=True).astype(float)
        df['VL_SALDO_FINAL'] = df['VL_SALDO_FINAL'].replace({',': '.'}, regex=True).astype(float)
        
        # Salvar o arquivo CSV corrigido
        df.to_csv(output_file, index=False, sep=';', encoding='UTF8')
        print(f'Arquivo corrigido gerado: {output_file}')
    
    except Exception as e:
        print(f'Erro ao processar {input_file}: {e}')
