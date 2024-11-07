def message(key):
    print(MSGS[key])


def projects_list(projects_data, with_paths: False):
    if with_paths:
        for project in projects_data.items():
            name, data = project
            print(f"{name}:\t{data["path"]}")
    else:
        for project in projects_data:
            print(project)


def usage(arg=""):
    if not arg:
        print(USAGE["app"])
    elif arg not in USAGE:
        print(f"'{arg}' is not a recognized command.\n")
        print(USAGE[arg])
        return
    else:
        print(USAGE[arg])


def no_path(path):
    print(f"Path '{path}' does not exist.\n")


def project_name_exists(name):
    print(f"Name '{name}' exists in projects.")
    print("Please use a unique name.\n")


def project_added_successfully(name):
    print(f"'{name}' added to projects.\n")


USAGE = {
        "app": "Usage: unpause [project-name | command] [args]\n",
        "add": "Usage: unpause add [name] [path/to/script]\n",
        }

MSGS = {
        "no_data": "No projects exists yet.\n",
        }