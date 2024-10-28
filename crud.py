import os
import pickle


PROJ_INDEX = "data/data.pickle"
PROJ_DIR = "projects"


def read_projects_data() -> dict:
    '''Read project data and return it as a dict.'''
    with open(PROJ_INDEX, 'rb') as file:
        projects_data = pickle.load(file)
    return projects_data


def write_projects_data(projects_data: dict):
    '''Write project data dict to pickle file.'''
    with open(PROJ_INDEX, "wb") as file:
        pickle.dump(projects_data, file)


def make_project_dir(name):
    '''Make a new directory for a project and return the realpath.'''
    dir_path = os.path.join(PROJ_DIR, name)
    # if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    return os.path.realpath(dir_path)


def write_script_file(script: str, path: str):
    '''Write a script file given the script template and file path.'''
    with open(path, 'w+') as file:
        file.write(script)


