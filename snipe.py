import requests
import os
import pandas as pd
import time

# Configurações da API
SNIPE_IT_URL = 'http://ipSnipeIT/api/v1'
API_TOKEN = 'Token API SnipeIT'

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json'
}

def fetch_assets():
    assets = []
    page = 1
    while True:
        try:
            response = requests.get(f'{SNIPE_IT_URL}/hardware?page={page}', headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if 'rows' not in data or not data['rows']:
                break
            assets.extend(data['rows'])
            print(f'Página {page} processada com {len(data["rows"])} ativos.')
            if 'total' in data and 'rows' in data:
                total_pages = data['total'] // len(data['rows']) + 1
                if page >= total_pages:
                    break
            page += 1
            time.sleep(1)  # Espera de 1 segundo entre as requisições para evitar sobrecarregar o servidor
        except requests.exceptions.RequestException as e:
            print(f'Erro na página {page}: {e}')
            break
    return assets

def save_to_csv(assets, file_name='ativosSnipe.csv'):
    df = pd.DataFrame(assets)
    df_filtered = df[['asset_tag', 'category', 'assigned_to']]
    df_filtered.to_csv(file_name, index=False)

if __name__ == "__main__":
    assets = fetch_assets()
    if assets:
        save_to_csv(assets)
        print(f'{len(assets)} ativos foram salvos no arquivo ativosSnipe.csv')
        
    else:
        print('Nenhum ativo foi encontrado ou ocorreu um erro durante a busca.')
