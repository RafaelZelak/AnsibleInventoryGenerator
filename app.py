import csv
import os
try:
    print(f'Iniciando Conexão com ActiveDirectory\n')
    os.system('python ad.py')
    print(f'Iniciando Conexão via API com o SnipeIT\n')
    os.system('python snipe.py')
    print(f'Organizando Resultados....\n')
    os.system('python cleanCsv.py')
    print(f'\n------ Todos os arquivos e APIs obtiveram exito! ------\n')
except:
    print(f'Houve um Erro ao Gerar os Arquivos de Configuração Via API\n')
def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.reader(csvfile))

def format_name(name):
    parts = name.split()
    first_name = parts[0].lower()
    last_name = parts[-1].lower()
    return f"{first_name}.{last_name}"

def get_active_number(name, dados):
    formatted_name = format_name(name)
    for record in dados:
        if record[2].lower() == formatted_name:
            return record[0]
    return "ST0000"

def write_to_files(setores):
    # Cria a pasta result se não existir
    print('Gerando Pasta com Resultados...\n')
    os.makedirs('result', exist_ok=True)
    
    # Escrever Setup.txt
    print('Gerando arquivos...\n')
    with open('result/Setup.txt', 'w', encoding='utf-8') as setup_file:
        for setor, users in setores.items():
            setup_file.write(f"#{setor}\n")
            for user in users:
                setup_file.write(f"{user}\n")
            setup_file.write("\n")
    
    # Escrever arquivos separados por setor
    for setor, users in setores.items():
        file_path = os.path.join('result', f'{setor}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            for user in users:
                file.write(f"{user}\n")

def main():
    # Ler os arquivos CSV
    usuarios_ldap = read_csv('usuarios_ldap.csv')
    dados = read_csv('dados.csv')

    # Dicionário para armazenar os usuários por setor
    setores = {}

    # Processar os dados do usuarios_ldap
    for setor, name in usuarios_ldap:
        if setor not in setores:
            setores[setor] = []
        active_number = get_active_number(name, dados)
        if active_number != "ST0000":
            formatted_user = f"{name.replace(' ', '')}_{active_number} ansible_host={active_number}"
            setores[setor].append(formatted_user)

    # Escrever os resultados em arquivos
    write_to_files(setores)
    print('Gerado com sucesso!')
if __name__ == '__main__':
    main()
