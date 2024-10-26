import os
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
        CMDS[args[0]](args)


def list_projects(args):
    print("listing!")


def add_project(args):
    print("adding project!")


def remove_project(args):
    print("removing")


def update_project(args):
    print("update")


def edit_project(args):
    print("edit")


def init_project(args):
    print("init")


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
