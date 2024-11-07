import os
import pickle
import subprocess


PROJ_INDEX = "data/data.pickle"
PROJECTS_DIR = "projects"


def add_project(name, path):
    projects_data = read_projects_data()
    if name in projects_data:
        return False
    projects_data[name] = {
            "path": path,
            }
    write_projects_data(projects_data)
    return True


def read_projects_data() -> dict:
    '''Read project data and return it as a dict.'''
    if not os.path.exists(PROJ_INDEX):
        write_projects_data({})
    with open(PROJ_INDEX, 'rb') as file:
        projects_data = pickle.load(file)
    return projects_data


def write_projects_data(projects_data: dict):
    '''Write project data dict to pickle file.'''
    with open(PROJ_INDEX, "wb") as file:
        pickle.dump(projects_data, file)


def make_project_dir(name):
    '''Make a new directory for a project and return the realpath.'''
    dir_path = os.path.join(PROJECTS_DIR, name)
    # if not os.path.exists(dir_path):
    os.makedirs(dir_path, exist_ok=False)
    return os.path.realpath(dir_path)


def write_file(script: str, path: str):
    '''Write a script file given the script template and file path.'''
    with open(path, 'w+') as file:
        file.write(script)


def make_exec(file_path: str):
    subprocess.run(["chmod", "+x", file_path])
