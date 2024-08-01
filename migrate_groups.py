import tableauserverclient as TSC

tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}', \
                        site_id = '')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new}',\
                        site_id = '')
server_new = TSC.Server('IP_address', use_server_version = True)

# Pull group data from old server
with server.auth.sign_in(tableau_auth):
    all_groups, pagination_item = server.groups.get()

# Post to new server
with server_new.auth.sign_in(tableau_auth_new):
    for i in all_groups:
        if i.name != 'All Users':
            server_new.groups.create(i)