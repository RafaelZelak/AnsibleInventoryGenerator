import requests
import os
import pandas as pd
import time

# Configurações da API
SNIPE_IT_URL = 'http://192.168.15.206//api/v1'
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNjYzNzlkZDQ4MmEwZjVhNzE1YjRkNzIxMjU3MTJjMjM1YmRhOGQ1NzZmNjdjNjQ0ZTgwMThiNzMwNThjMTg1N2IzYThlN2JkNjYyYmFkNGEiLCJpYXQiOjE3MjM1NzQyOTkuODE3NTIyLCJuYmYiOjE3MjM1NzQyOTkuODE3NTI2LCJleHAiOjIxOTY4NzM0OTkuODA5MjQ2LCJzdWIiOiIxNTAiLCJzY29wZXMiOltdfQ.HX6Jem0pPMxZUqkcatGjjUM8EKYhbAwiHP1S5Gulr40pozQRnrCVXweuIeloTDbx9ACpXO351zcNamMF2UYOv4q-3j9JWxmumslYz2wb3SN0ovRCCSgKMB6K2xgc9eygLbbdh5uDVI4x8sC2j0i_8t8nsiJTzmL-TRkkEgvwYWpqNYZybwc2404qnhHUmdcsyb3EAXHUnfGw7f6xzv_LOaF0T6t-il7s7z2ErV1w3UmRFukUZbxL7mGnIs-HTuKh0iGw8iX3ZaxBbFc38S-9QpbVmOuKzP7F2ZO_F8TU-Fbc2jF9Tkafpe-CfgsQoN1b0Js1VuEJeZ9FFgDIOQRohyAi40e7VYhdMFtSEF-A5wpKocz79rh1sAazAvXdVZD0qfWBb4wJ_s6zdbbBNqBjJs_x1SpbwzNKS6FUXSeArnIGLk5HoyZhDnSve7JEdaY7TkCTss1nS4L_S6rLdd3E8JjTKOdTM7ehiSMjzcWAyBO_orQEXx8Olj6ujiVRrbaMBZtsw5HFfcNFy4Oh_VCX9gEMMbBMqRvP6Hs1HKdXZpswFlsfH8EArXss39D9lUL6xzJsqWE-yMjNdHz6pIxqJZZSyJB7vw49EEbsUQX-zn23xB11iTQVGG1eJX0LBTQJhxPrEqVjb0q_1DbmwdI0nQhCwtVJnMmJ8g9TT5QWLR0'

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
