import os
import shutil
import subprocess
from sys import argv


def main():
    if len(argv) < 2:
        print("no args")
        return
    else:
        args = argv[1:]
    if not args[0] in CMDS:
        print("not in commands")
    else:
        CMDS[args[0]]()


def list_projects():
    print("listing!")


def add_project():
    print("adding project!")


def remove_project():
    print("removing")


def update_project():
    print("update")


def edit_project():
    print("edit")


def init_project():
    print("init")


def set_home():
    print("setting home")


CMDS = {
        "list": list_projects,
        "add": add_project,
        "remove": remove_project,
        "update": update_project,
        "edit": edit_project,
        "init": init_project,
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
