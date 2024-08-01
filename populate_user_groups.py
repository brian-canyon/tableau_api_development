import tableauserverclient as TSC
import json

tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}', \
                                site_id = '')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new}',\
                                site_id = '')
server_new = TSC.Server('{IP_address_new}', use_server_version = True)

with open('user_groups_dict') as f:
    data = f.read()

data = data.replace("\'", "\"")
js = json.loads(data)

with server_new.auth.sign_in(tableau_auth_new):
        all_users_asc = []
        all_users_desc = []
        request_options = TSC.RequestOptions(pagesize = 1000)
        request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Direction.Asc))
        all_users_asc, pagination_item = server_new.users.get(req_options = request_options)
        request_options = TSC.RequestOptions(pagesize = 570)
        request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name, TSC.RequestOptions.Direction.Desc))

        all_users_desc, pagination_item = server_new.users.get(req_options = request_options)

all_users_new = []
all_users_new = all_users_asc + all_users_desc

## PROBLEM STATEMENT: 
#       To post a user to a group, you need two things, the group name and !ID! of the user to post. The ID of each
#       user changed as we went from the new server to the old server. To make things even more fun, the name of many
#       users also changed in the migration. Unsure how or why, but it needs to be explored

## What we have now:
#       Two things. A dictionary containing names (from the old server) and he groups they reside in. Also a item,
#       'all_users' that contains name and ID data of the users in

js_new = {}
for user in all_users_new:
    for key in js:
        if key == user.name:
            js_new[user.id] = js[key]
            



with server_new.auth.sign_in(tableau_auth_new):
    all_groups, _ = server_new.groups.get()
    for key, value in js_new.items():
        for i in value:
            
            for group in all_groups:
                if group.name == i:
                    try:
                        server_new.groups.add_user(group, key)
                        print("User added to " + group.name)
                    except Exception as error:
                        print(error)