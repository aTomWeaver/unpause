import crud


def print_projects_list():
    projects_data = crud.read_projects_data()
    for project in projects_data:
        print(project)
