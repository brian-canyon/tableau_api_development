import pandas as pd
import tableauserverclient as TSC

## Create authentication parameters to new and old server

# Old Server
tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}', \
        site_id = '')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new}',\
        site_id = '')
server_new = TSC.Server('{IP_address_new}', use_server_version = True)

## Pull user info ('get')
## TSC can only oull up to 1000 users at one time, to combat this, the below code pulls the top 1000 users
## foloowed by the bottom 1000 users and creates two different lists. Later deleting the duplicates
## The below strategy assumes the number of users is between 1000 and 2000 (1687 current)

with server.auth.sign_in(tableau_auth):
    all_users_asc = []
    all_users_desc = []
    request_options = TSC.RequestOptions(pagesize = 1000)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                            TSC.RequestOptions.Direction.Asc))
    all_users_asc, pagination_item = server.users.get(req_options = request_options)
    request_options = TSC.RequestOptions(pagesize = 1000)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                            TSC.RequestOptions.Direction.Desc))

    all_users_desc, pagination_item = server.users.get(req_options = request_options)

## These two lists will be appended together and drop duplicates
## Tableau cannot create users with site_permissions 'serveradmin..'

user_id_desc = []
for user in all_users_desc:
    user_id_desc.append(user.id)

for user in all_users_asc:
    if user.id in user_id_desc:
        all_users_asc.remove(user)
all_users = []
all_users = all_users_asc + all_users_desc
for i in all_users:
    if i.site_role == 'ServerAdministrator':
        all_users.remove(i)



## Since some users have already been added, we need to remove any users that exist already on both sites
## This can be done by throwing a get request at the new site and removing duplicates

with server_new.auth.sign_in(tableau_auth_new):
    request_options = TSC.RequestOptions(pagesize = 1000)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                            TSC.RequestOptions.Direction.Asc))
    users_asc_new, _ = server_new.users.get(req_options = request_options)
    request_options = TSC.RequestOptions(pagesize = 517)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                            TSC.RequestOptions.Direction.Desc))

existing_users = users_asc_new + users_desc_new
existing_user_name = []
for i in existing_users:
    existing_user_name.append(i.name)


for i in all_users:
    if i.name in existing_user_name:
        all_users.remove(i)

## Post new users ('add')
print("length of list that adds users:")
print(len(all_users))
with server_new.auth.sign_in(tableau_auth_new):
   for i in all_users:
        try:
            server_new.users.add(i)
            print("User " + i.name + " added sucsessfully!")
        except:
            print("user " + i.name +  "XX  COULD NOT BE PUBISHED XX  ")