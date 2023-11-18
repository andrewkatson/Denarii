# Helps in finding the current workspace path.

import os
import pathlib

def find_workspace_path():
    workspace_path = pathlib.Path()

    # Need to explicitly set this or pass it in as a variable.
    linux_workspace_path = pathlib.Path("/home/andrew/denarii")
    windows_workspace_path = pathlib.Path("C:/Users/katso/Documents/Github/denarii")

    # A workspace path that works if not sudo on EC2
    try:
        possible_workspace_path = pathlib.Path(os.environ["HOME"] + "/denarii")
        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("The HOME variable does not point to the directory")

    # A workspace path that works in sudo on EC2
    try:
        possible_workspace_path = pathlib.Path("/home/" + os.environ["SUDO_USER"] + "/denarii")

        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("Not on an EC2 using sudo")

    # A workspace path that works on Windows
    try:
        possible_workspace_path = pathlib.Path(
            os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + "\\Documents\\Github\\denarii")

        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("Not on Windows")

    if os.path.exists(linux_workspace_path):
        workspace_path = linux_workspace_path
    elif os.path.exists(windows_workspace_path):
        workspace_path = windows_workspace_path

    return workspace_path


def get_home():
    linux_home = pathlib.Path()
    windows_home = pathlib.Path()

    try:
        linux_home = pathlib.Path(os.environ["HOME"])
    except Exception as e:
        print(e)
    try:
        windows_home = pathlib.Path(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"])
    except Exception as e:
        print(e)

    if os.path.exists(linux_home):
        return linux_home
    else:
        return windows_home


def find_other_workspace_path(workspace_name):
    workspace_path = pathlib.Path()
    # A workspace path that works if not sudo on EC2
    try:
        possible_workspace_path = pathlib.Path(os.environ["HOME"] + "/" + workspace_name)
        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("The HOME variable does not point to the directory")

    # A workspace path that works in sudo on EC2
    try:
        possible_workspace_path = pathlib.Path("/home/" + os.environ["SUDO_USER"] + "/" + workspace_name)

        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("Not on an EC2 using sudo")

    # A workspace path that works on Windows
    try:
        possible_workspace_path = pathlib.Path(
            os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + "\\Documents\\Github\\" + workspace_name)

        if os.path.exists(possible_workspace_path):
            workspace_path = possible_workspace_path
    except Exception as e:
        print(e)
        print("Not on Windows")

    return workspace_path
