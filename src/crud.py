import os
import pickle
import subprocess


PROJ_INDEX = "data/data.pickle"
PROJECTS_DIR = "projects"


# data schema
ps = {
        "project_name": {
            "entry_point": "entry_point.sh",
            "files": {
                "entry_point.sh": "text content_of_entry_point_script",
                "name_of_file.txt": "text content_of_file",
                "name_of_file2.txt": "text content_of_file2",
                "name_of_file3.txt": "text content_of_file3",
                }
            }
        }


def add_project(name, path, files={}):
    projects_data = read_projects_data()
    if name in projects_data:
        return False
    projects_data[name] = {
            "entry_point": path,
            "files": files
            }
    write_projects_data(projects_data)
    cache_all()
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


def cache_all():
    project_dirs = os.listdir(os.path.realpath(PROJECTS_DIR))
    for pdir in project_dirs:
        print(pdir)


if __name__ == "__main__":
    cache_all()
    print(read_projects_data())
