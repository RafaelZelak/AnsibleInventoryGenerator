import unicodedata
from ldap3 import Server, Connection, ALL
import requests
from config import API_TOKEN

# Configurações da API Snipe-IT
SNIPEIT_URL = 'http://192.168.15.206/api/v1/'
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Configurações do servidor e credenciais LDAP
AD_SERVER = 'digitalup.intranet'
AD_USER = 'administrator'
AD_PASSWORD = '&ajhsRlm88s!@SF'

# Função para normalizar strings, removendo acentos e caracteres especiais
def normalize_string(text):
    if not text:
        return text
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

# Função para buscar ativos
def get_assets():
    url = f'{SNIPEIT_URL}hardware'
    params = {
        'limit': 500,
        'offset': 0
    }

    all_assets = []
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar ativos: {response.status_code}")
            print(response.json())
            return []

        data = response.json()
        all_assets.extend(data['rows'])

        if len(data['rows']) < params['limit']:
            break
        params['offset'] += params['limit']

    return all_assets

# Função para consultar o LDAP e buscar a OU do usuário
def get_user_ou(username):
    try:
        server = Server(AD_SERVER, get_info=ALL)
        conn = Connection(server, user=f'{AD_USER}@{AD_SERVER}', password=AD_PASSWORD, auto_bind=True)

        search_base = 'DC=digitalup,DC=intranet'
        search_filter = f'(sAMAccountName={username})'

        conn.search(search_base=search_base, search_filter=search_filter, attributes=['distinguishedName'])

        if conn.entries:
            dn = conn.entries[0].distinguishedName.value
            # Extraindo a OU do DN
            ou_parts = [part for part in dn.split(',') if part.startswith('OU=')]
            ou_name = ou_parts[0].replace('OU=', '') if ou_parts else 'Sem setor'
            return normalize_string(ou_name)
    except Exception as e:
        print(f"Erro ao buscar OU no LDAP para {username}: {e}")
    return 'Sem setor'  # Retorna uma string padrão em caso de falha

# Função para filtrar ativos e pegar o status
def filter_and_check_assets(assets):
    target_types = ['desktop', 'notebooks', 'allinone']
    results = []

    for asset in assets:
        hardware_type = asset['category']['name'].lower()
        if hardware_type in target_types:
            status_label = asset['status_label']['name'].lower()
            if 'em uso' in status_label:
                assigned_user = None
                if asset.get('assigned_to') and 'username' in asset['assigned_to']:
                    assigned_user = asset['assigned_to']['username']

                if assigned_user:
                    if '16º' in assigned_user or '17º' in assigned_user:
                        continue

                    asset_tag = asset.get('asset_tag', 'Sem marcação')
                    user_ou = get_user_ou(assigned_user)

                    results.append({
                        'username': assigned_user,
                        'asset_tag': asset_tag,
                        'ou': user_ou
                    })

    return results

# Função para salvar os resultados em um arquivo TXT no formato Ansible
def save_to_txt(filtered_assets):
    with open('inventory.ini', 'w') as file:
        file.write('[windows]\n')
        for asset in filtered_assets:
            ou = str(asset.get('ou', 'Sem setor')).lower()  # Garante que 'ou' é sempre uma string
            line = f"{asset['username']}_{asset['asset_tag']} ansible_host={asset['asset_tag']} #{asset['ou']}\n"

            # Comenta a linha inteira se o setor for Desenvolvimento
            if ou == 'desenvolvimento':
                line = f"# {line}"

            file.write(line)

        # Escreve a seção [windows:vars]
        file.write('\n[windows:vars]\n')
        file.write('ansible_user=administrator\n')
        file.write('ansible_password=&ajhsRlm88s!@SF\n')
        file.write('ansible_port=5985\n')
        file.write('ansible_connection=winrm\n')
        file.write('ansible_winrm_transport=ntlm\n')
        file.write('ansible_winrm_server_cert_validation=ignore\n')


# Executando o script
if __name__ == "__main__":
    print("Buscando ativos no Snipe-IT...")
    assets = get_assets()

    if not assets:
        print("Nenhum ativo encontrado.")
    else:
        print("Filtrando ativos relevantes...")
        filtered_assets = filter_and_check_assets(assets)

        print("\nAtivos em uso encontrados:")
        for asset in filtered_assets:
            print(f"Nome: {asset['username']}, Tipo: {asset['asset_tag']}, Setor: {asset['ou']}")

        print("\nSalvando no arquivo inventory.ini...")
        save_to_txt(filtered_assets)
        print("Arquivo 'inventory.ini' salvo com sucesso!")
