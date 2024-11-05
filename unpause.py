import os
import crud
from scripts import ScriptBuilder
import printing
import shutil
import subprocess
from sys import argv


def main():
    if len(argv) < 2:
        print("no args")
        return
    else:
        command = argv[1]
        if len(argv) > 2:
            args = argv[2:]
        else:
            args = []
    if command not in CMDS:
        print(f"\"{command}\" not in commands.\n")
        print_usage()
    else:
        CMDS[command](args)


def list_projects(args):
    print("listing!")
    printing.print_projects_list()


def add_project(args):
    print("adding project!")


def remove_project(args):
    print("removing")


def update_project(args):
    print("update")


def edit_project(args):
    print("edit")


def init_project(args):
    options = ["tmux", "firefox"]
    name = args[0]
    if "-p" in args[1:]:
        programs = args[args.index("-p") + 1:]
    else:
        print(f"Options: [{options}]")
        programs = input("Which programs would you like to use?\n ").replace(",", " ").split(" ")
    print(programs)
    return
    script_name = input("What would you like to call it?\n\t> ")
    path = input("Where should it start?\n\t> ")
    script = ScriptBuilder(script_name)
    script.tmux_init()

    build_data = script.build()
    url_queue = build_data["url_queue"]
    script_string = build_data["script"]
    project_dir = crud.make_project_dir(build_data["dir_path"])
    script_path = os.path.join(project_dir, f"{script_name}.sh")
    if url_queue != []:
        for item in url_queue:
            name, url = item
            crud.write_file(url, os.path.join(project_dir, name))
    crud.write_file(script_string, script_path)
    crud.make_exec(script_path)


def set_home(args):
    print("setting home")


def print_usage(args):
    print("Usage: unpause [project-name | command] [args]")


CMDS = {
        "list": list_projects,
        "l": list_projects,
        "ls": list_projects,
        "add": add_project,
        "a": add_project,
        "remove": remove_project,
        "rm": remove_project,
        "r": remove_project,
        "update": update_project,
        "u": update_project,
        "edit": edit_project,
        "e": edit_project,
        "init": init_project,
        "i": init_project,
        "set-home": set_home,
        }


COLORS = {
        "header": '\033[95m',
        "blue": '\033[94m',
        "cyan": '\033[96m',
        "green": '\033[92m',
        "warning": '\033[93m',
        "fail": '\033[91m',
        "end": '\033[0m',
        "bold": '\033[1m',
        "underline": '\033[4m',
        }


if __name__ == "__main__":
    main()
