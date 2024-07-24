import csv
from ldap3 import Connection, Server, ALL_ATTRIBUTES, SUBTREE

try:
    server = Server('dominio.intranet', get_info=ALL_ATTRIBUTES)
    con = Connection(server, user='userAdmin@dominio', password='senhaUserAdmin', auto_bind=True)

    search_base = 'DC=dominio,DC=intranet'
    search_filter = '(objectClass=organizationalUnit)'
    attributes = ['distinguishedName', 'name']

    con.search(search_base, search_filter, attributes=attributes, search_scope=SUBTREE)

    formatted_results = []

    for entry in con.entries:
        unidade_organizacional = str(entry.name)

        if unidade_organizacional.lower() == 'users':
            continue

        users_filter = '(objectClass=user)'
        users_search_base = entry.entry_dn
        con.search(users_search_base, users_filter, attributes=['cn'])

        for user_entry in con.entries:
            usuario = str(user_entry.cn)
            formatted_results.append([unidade_organizacional, usuario])

    with open('usuarios_ldap.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Unidade Organizacional', 'Usuário'])
        writer.writerows(formatted_results)

    print("Os dados foram salvos em usuarios_ldap.csv")

except Exception as e:
    print(f"Ocorreu um erro durante a busca: {e}")
