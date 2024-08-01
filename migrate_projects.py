import tableauserverclient as TSC
import pandas as pd
## Create authentication parameters to new and old server

# Old Server
tableau_auth = TSC.PersonalAccessTokenAuth('{token_name}', '{token_value}', \
                site_id = '')
server = TSC.Server('{IP_address}', use_server_version = True)

# New Server
tableau_auth_new = TSC.PersonalAccessTokenAuth('{token_name_new}', '{token_value_new',\
                site_id = '')
server_new = TSC.Server('{IP_address_new', use_server_version = True)

with server.auth.sign_in(tableau_auth):
    all_project_items, pagination_item = server.projects.get()
    proj_name = []
    proj_parent_id = []
    proj_desc = []
    for project in all_project_items:
        proj_name.append(project.name)
        proj_parent_id.append(project.parent_id)
        proj_desc.append(project.description)
    proj_parent_name = []
    for parent in proj_parent_id:
        if parent != None:
            for project in all_project_items:
                if parent == project.id:
                    proj_parent_name.append(project.name)
        else:
            proj_parent_name.append(None)



lists = [proj_name, proj_parent_id, proj_desc, proj_parent_name]
df = pd.DataFrame(list(zip(proj_name, proj_parent_id, proj_desc, proj_parent_name)), \
        columns = ['Name', 'parent_id_old', 'description', 'parent_name'])



with server_new.auth.sign_in(tableau_auth_new):
    all_project_items, pagination_item = server_new.projects.get()
    proj_parent_id = []
    current_proj_names = []
    for project in all_project_items:
        current_proj_names.append(project.name)
    for name in proj_parent_name:
        if name != None:
            if name in current_proj_names:
                for project in all_project_items:
                    if name == project.name:
                        proj_parent_id.append(project.id)
            else:
                    proj_parent_id.append(None)
        else:
            proj_parent_id.append(None)
    
    

    df['parent_id_new'] = proj_parent_id
    for index, row in df.iterrows():
        if row['Name'] not in current_proj_names and row['parent_id_new'] != None:
            new_project = TSC.ProjectItem(name = row['Name'], description = row['description'], \
                    parent_id = row['parent_id_new'])
            try:
                server_new.projects.create(new_project)
                print("!! " + row['Name'] + " !!")
            except:
                print("Failed to create " + new_project.name)