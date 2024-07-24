# LDAP User Exporter (Arquivo `ad.py`)

Este projeto é uma ferramenta para exportar usuários de unidades organizacionais específicas de um Active Directory (AD) para um arquivo CSV.

## Pré-requisitos

- Python 3.x
- Bibliotecas necessárias:
```sh
pip install ldap3
````
- Servidor LDAP
- Servidor Ansible
## Como Usar

Modifique as informações de:

  ```python
  server = Server('dominio.intranet', get_info=ALL_ATTRIBUTES)
````
Colocando o nome do seu dominio do Active Directory

Após isso adicione as informações do ADM para acessar o AD

```python
con = Connection(server, user='userAdmin@dominio', password='senhaUserAdmin', auto_bind=True)
````

Colocar as informações:

**User=''**
Em user coloque o nome de um usuario administrador e após o @ o domínio que ele pertence;

**password=''**
Basta colocar a senha referente ao usuário adicionado;

**search_base = 'DC='**
Adicione após o 'DC=' novamente o nome do seu Servidor AD. 

#### No caso do meu projeto, meu domínio tem .intranet após o nome, caso o seu não tenha siga os seguintes passos:

  ```python
  server = Server('dominio', get_info=ALL_ATTRIBUTES)
````
Na variável `server` coloque apenas o dominio sem o .intranet

Agora na variável `search_base` que está assim:

```python
search_base = 'DC=dominio,DC=intranet'
````
Modifique removendo um dos `DC=`. 
Ficando assim:

```python
search_base = 'DC=dominio'
````

# Gerar Pasta com arquivos padronizados para Inventory Ansible(Arquivo `app.py`)

Este script Python gera arquivos padronizados para uso como Inventory no Ansible, organizando os usuários por setor.

## Descrição

Este projeto lê dados de um arquivo CSV e de um arquivo CSV gerado pelo ad.py que pegou as informações do LDAP para gerar arquivos de configuração formatados para o Ansible, separados por setor.

## Requisitos

- Python 3.x
- Arquivos de entrada:
  - `dados.csv`: Contém informações dos usuários.
  - `usuarios_ldap.csv`: Relaciona os usuários aos seus respectivos setores (gerado automaticamente após realizar as configurações do `ad.py`).
  
## Funcionalidades

- Formatação de nomes para garantir compatibilidade.
- Geração de arquivos por setor com informações necessárias para o Ansible.

## Uso

1. Modifique o arquivo `ad.py` para acessar seu servidor LDAP (Active Directory)
2. Certifique-se de ter o arquivos `dados.csv`corretamente preenchido. (Nas proximas linhas demonstrarei como ele deverá ficar)
3. Execute o script Python `app.py`.
4. O script irá gerar arquivos de configuração por setor na pasta `result/` e um arquivo de saída geral em `result/Setup.txt` ou em arquivos `.txt` separados por setor.

   
## Config `dados.csv`

O arquivo `dados.csv` deverá conter as informações:

```csv
Hostname,InfoControle,Username
Hostname,InfoControle,Username
Hostname,InfoControle,Username
````

No caso `Hostname` é o proprio Hostname dos Hosts Windows conectados a sua Intranet, também pode ser o IP
###### Para ter este controle pode utilizar OCS Inventory ou outros sistemas de organização que forneçam um relatório `.csv`

Já a `InfoControle` é qualquer informação de controle (não será usada no código)
###### Usei por exemplo que tipo de equipamento é Desktop ou Notebook

E `Username` é o nome da pessoa que está com o Equipamento, deve bater com o nome cadastrado no Active Directory ou caso não esteja usando LDAP devem estar pelo menos preenchido o arquivo `usuarios_ldap.csv`

O arquivo `usuarios_ldap.csv` deve ser configurado seguindo o seguinte padrão:

```csv
UnidadeOrganizacional(Setor),Username
UnidadeOrganizacional(Setor),Username
UnidadeOrganizacional(Setor),Username
````

Após isso, basta executar o arquivo `app.py` e ver o resultado na pasta `result/`

Resultado:

```ini
#Setor(Unidade Organizacional Do LDAP)
Username_Hostname ansible_host=Hostname
````

No caso o Hostname pode ser o IP

Caso queira desvincular o `app.py` do `ad.py` basta remover a seguinte linha logo no começo do aruquivo `app.py`

```python
os.system('python ad.py')
````

E para adicionar no Ansible, basta ao gerar o `inventory.ini` padronizado com Winrm para rodar em hosts Windows

```ini
[windows]
Username_Hostname ansible_host=Hostname
Username_Hostname ansible_host=Hostname
Username_Hostname ansible_host=Hostname
[...]

[windows:vars]
ansible_user=adminDaIntranet
ansible_password=passwordDoAdmin
ansible_port=5985
ansible_connection=winrm
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
````

# API Snipe-IT
###### Opicional

## Introdução
Este projeto fornece scripts em Python para integrar-se à API do SnipeIT e gerenciar ativos de hardware. Ele inclui funcionalidades para buscar ativos da API e salvá-los em um arquivo CSV, bem como limpar e filtrar os dados extraídos.

## Pré-requisitos
Python 3.x

Bibliotecas: `requests`, `pandas`
### Configuração
Clone o repositório.
Instale as dependências necessárias:
````sh
pip install requests pandas
````
### Scripts
1 - snipe.py
Este script busca os ativos de hardware do SnipeIT e os salva em um arquivo CSV.

## Configurações da API:

Defina as variáveis `SNIPE_IT_URL` e `API_TOKEN` com a URL da API do SnipeIT e o token de autenticação, respectivamente.
Funções principais:

`fetch_assets()`: Faz requisições paginadas à API do SnipeIT para buscar todos os ativos de hardware. Em caso de erro, a execução para e uma mensagem de erro é exibida.
save_to_csv(assets, file_name='ativosSnipe.csv'): Salva os dados dos ativos em um arquivo CSV, mantendo apenas as colunas asset_tag, category e assigned_to.
Execução:

Execute o script para buscar os ativos e salvá-los em um arquivo CSV:
````sh
python snipe.py
````
O arquivo resultante será `ativosSnipe.csv`.

2 - cleanCsv.py

Este script limpa e filtra os dados extraídos dos ativos, focando em categorias específicas e removendo o cabeçalho do CSV.

### Funções principais:

`extract_category(category_str)`: Extrai o nome da categoria a partir de uma string de dicionário.
`extract_username(assigned_to_str)`: Extrai o nome de usuário do responsável a partir de uma string de dicionário.
`filter_categories(category)`: Filtra as linhas com categorias específicas, neste caso, Notebooks e Desktop.
## Execução:

Execute o script para limpar e filtrar os dados do arquivo CSV gerado pelo script anterior:

````sh
python cleanCsv.py
````
O arquivo resultante será `dados.csv`, contendo apenas as colunas asset_tag, category e assigned_to.
## Conclusão
Esses scripts automatizam o processo de extração, limpeza e filtragem de dados de ativos do SnipeIT, facilitando a gestão dos ativos de hardware. Ajuste as configurações conforme necessário e execute os scripts para obter os resultados desejados.




