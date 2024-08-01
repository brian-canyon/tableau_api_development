import tableauserverclient as TSC
import pandas as pd
## Create authentication parameters to new and old server

# Old Server
tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new}', site_id= '')
server_new = TSC.Server('{IP_address_new}', use_server_version = True)

with server.auth.sign_in(tableau_auth):
    all_users_asc = []
    all_users_desc = []
    request_options = TSC.RequestOptions(pagesize = 1000)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                                    TSC.RequestOptions.Direction.Asc))
    all_users_asc, pagination_item = server.users.get(req_options = request_options)
    request_options = TSC.RequestOptions(pagesize = 574)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                                     TSC.RequestOptions.Direction.Desc))
    all_users_desc, _ = server.users.get(req_options = request_options)
    all_users_old = []
    all_users_old = all_users_desc + all_users_asc

    request_options = TSC.RequestOptions(pagesize = 300)
    all_workbooks, _ = server.workbooks.get(req_options = request_options)
    owner_id_list = []
    workbook_name_list = []
    for workbook in all_workbooks:
        workbook_name_list.append(workbook.name)
        owner_id_list.append(workbook.owner_id)
        
    print(len(workbook_name_list))
    owner_name_list = []
    for owner in owner_id_list:
        for user in all_users_old:
            if user.id == owner:
                owner_name_list.append(user.name)
    lists = [owner_id_list, workbook_name_list, owner_name_list]
    old_df = pd.DataFrame(list(zip(owner_name_list, workbook_name_list)),
            columns = ['owner name', 'workbook name'])

    print(old_df)

with server_new.auth.sign_in(tableau_auth_new):
    request_options = TSC.RequestOptions(pagesize = 300)
    all_workbooks, _ = server_new.workbooks.get(req_options = request_options)
    all_users_desc = []
    request_options = TSC.RequestOptions(pagesize = 1000)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                                    TSC.RequestOptions.Direction.Asc))
    all_users_asc, pagination_item = server_new.users.get(req_options = request_options)
    request_options = TSC.RequestOptions(pagesize = 570)
    request_options.sort.add(TSC.Sort(TSC.RequestOptions.Field.Name,
                                    TSC.RequestOptions.Direction.Desc))
    all_users_desc, _ = server_new.users.get(req_options = request_options)

    all_users_old = []
    all_users_new = all_users_desc + all_users_asc
    owner_id_list_new = []
    workbook_name_list_new = []
    new_users_dict = {}
    for user in all_users_new:
        new_users_dict[user.name] = user.id
    for workbook in all_workbooks:
        for index, row in old_df.iterrows():
            if workbook.name == row['workbook name']:
                try:
                    user_id = new_users_dict[row['owner name']]
                    workbook.owner_id = user_id
                    server_new.workbooks.update(workbook)
                    print(workbook.name + " has been updated")
                except:
                    print(workbook.name + " THREW AN ERROR!!")