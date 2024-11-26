import pandas as pd
import ast

# Função para extrair o valor desejado das strings
def extract_category(category_str):
    try:
        category_dict = ast.literal_eval(category_str)
        return category_dict.get('name', '')
    except (ValueError, SyntaxError):
        return ''

def extract_username(assigned_to_str):
    try:
        assigned_to_dict = ast.literal_eval(assigned_to_str)
        return assigned_to_dict.get('username', '')
    except (ValueError, SyntaxError):
        return ''

# Função para filtrar as categorias desejadas
def filter_categories(category):
    return category in ['Notebooks', 'Desktop']

# Caminho para o arquivo CSV original e o arquivo limpo
input_file = 'ativosSnipe.csv'
output_file = 'dados.csv'

# Lê o arquivo CSV original
df = pd.read_csv(input_file)

# Aplica a limpeza e extração das colunas
df['category'] = df['category'].apply(extract_category)
df['assigned_to'] = df['assigned_to'].apply(extract_username)

# Filtra as linhas com as categorias desejadas
df_filtered = df[df['category'].apply(filter_categories)]

# Renomeia as colunas para o formato desejado
df_cleaned = df_filtered[['asset_tag', 'category', 'assigned_to']]

# Salva o arquivo CSV limpo sem o cabeçalho
df_cleaned.to_csv(output_file, index=False, header=False)

print(f'Arquivo limpo, filtrado e sem cabeçalho salvo como {output_file}')