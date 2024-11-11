def message(key):
    print(MSGS[key])


def projects_list(projects_data, with_paths: False):
    longest_title = len(max(projects_data.keys(), key=len))
    if with_paths:
        for project in projects_data.items():
            name, data = project
            spacing = (longest_title - len(name) + 2) * " "
            print(f"{name}:{spacing}{data["path"]}")
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


def check_args(args, fn, min_len):
    if len(args) < min_len:
        usage(fn)
        return False
    return True


def no_path(path):
    print(f"Path '{path}' does not exist.\n")


def no_project(name):
    print(f"No project named '{name}' found.")


def project_name_exists(name):
    print(f"Name '{name}' exists in projects.")
    print("Please use a unique name.\n")


def project_added_successfully(name):
    print(f"'{name}' added to projects.\n")


USAGE = {
        "app": "Usage: unpause [project-name | command] [args]\n",
        "add": "Usage: unpause add [name] [path/to/script]\n",
        "remove": "Usage: unpause remove [name]\n",
        }

MSGS = {
        "no_data": "No projects exists yet.\n",
        }
