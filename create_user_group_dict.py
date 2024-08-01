import tableauserverclient as TSC

tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}', \
                        site_id = '')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new}',\
                        site_id = '')
server_new = TSC.Server('{IP_address_new}', use_server_version = True)

## Create a dictionary with user.name as a key and the groups they exist in as values
user_groups_dict = {}
with server.auth.sign_in(tableau_auth):
    all_groups, pagination_item = server.groups.get()
    for group in all_groups:
        if group.name != 'All Users':

            server.groups.populate_users(group)
            for user in group.users:
                if user.name not in user_groups_dict:
                    user_groups_dict[user.name] = []
                user_groups_dict[user.name].append(group.name)