# Helps in finding the current workspace path.

import argparse
import os
import pathlib

parser = argparse.ArgumentParser(description="Process command line flags")
parser.add_argument('--workspace_path', type=str, help='The path to the relevant WORKSPACE file', default='')

args = parser.parse_args()


def find_workspace_path():

    workspace_path = pathlib.Path()

    if args.workspace_path == '':
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
            possible_workspace_path = pathlib.Path(os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + "\\Documents\\Github\\denarii")
        except Exception as e:
            print(e)
            print("Not on Windows")

        if os.path.exists(linux_workspace_path):
            workspace_path = linux_workspace_path
        elif os.path.exists(windows_workspace_path):
            workspace_path = windows_workspace_path
    else:
        workspace_path = pathlib.Path(args.workspace_path)

    return workspace_path
