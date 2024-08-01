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
    request_options = TSC.RequestOptions(pagesize = 300)
    all_workbooks, _ = server.workbooks.get(req_options = request_options)
    file_path_list = []
    project_name_list = []
    project_id_list = []
    data_con_dict = {}
    workbook_name_list = []
    for workbook in all_workbooks:
        try:
            file_path = server.workbooks.download(workbook.id)
        except:
            print(workbook.name + "Casued an error")
        file_path_list.append(file_path)
        workbook_name_list.append(workbook.name)
        #server.workbooks.populate_connections(workbook) # Create dictionary to explain workbook/datasource
        ## relatioship
        #data_con_dict[workbook.name] = workbook.connections
        project_name_list.append(workbook.project_name)
        project_id_list.append(workbook.project_id)
    print(len(project_id_list))
    all_projects, _ = server.projects.get(req_options = request_options)
    proj_parentid_list = []
    for proj_id in project_id_list:
        for project in all_projects:
            if project.id == proj_id:
                proj_parentid_list.append(project.parent_id)
    proj_parentname_list = []

    for parent in proj_parentid_list:
        if parent == None:
            proj_parentname_list.append(None)
        else:
            for project in all_projects:
                if parent == project.id:
                    proj_parentname_list.append(project.name)

with server_new.auth.sign_in(tableau_auth_new):
    all_projects_new, _ = server_new.projects.get(req_options = request_options)
    proj_id_new = []
    proj_parent_id_new = []
    proj_name_new = []
    for project in all_projects_new:
        proj_id_new.append(project.id)
        proj_parent_id_new.append(project.parent_id)
        proj_name_new.append(project.name)

    proj_parent_name_new = []
    for id_new in proj_parent_id_new:
        if id_new == None:
            proj_parent_name_new.append(None)
        else:
            for project in all_projects_new:
                if project.id == id_new:
                    proj_parent_name_new.append(project.name)

    df_oldserver = pd.DataFrame(
                {'filepath': file_path_list,
                'project': project_name_list,
                'project parent name': proj_parentname_list,
                'workbook name': workbook_name_list
                })
    df_newserver = pd.DataFrame(
                {'project id': proj_id_new,
                'project': proj_name_new,
                'project parent name': proj_parent_name_new
                })
    joined_df = pd.merge(df_oldserver, df_newserver, how = 'left',\
                            left_on=['project', 'project parent name'],\
                            right_on=['project', 'project parent name'])

    counter = 0
    for index, row in joined_df.iterrows():
       new_workbook = TSC.WorkbookItem(project_id = row['project id'], name = row['workbook name'], show_tabs = True)
       try:
            server_new.workbooks.publish(new_workbook, row['filepath'], mode = ('Overwrite'), as_job = True)
            print(row['filepath'])
            print(("published"))
            counter = counter + 1
            print(counter)
       except:
            print(row['filepath'])
            print("ERROR")
            conter = counter + 1
            print(counter)