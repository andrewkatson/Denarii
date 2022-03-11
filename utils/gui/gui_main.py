# This is the main file for the Denarii gui.
# It assumes that https://github.com/andrewkatson/KeirosPublic is located at either
# %HOME/denarii or %HOMEDRIVE%%HOMEPATH%/Documents/Github/denarii

import sys
import workspace_path_finder

from tkinter import *
from tkinter import ttk

# Modify the PATH to include the path to the denarii python client
sys.path.append(str(workspace_path_finder.find_other_workspace_path("KeirosPublic") / "Client" / "Denarii"))

import denarii_client

# Modify the PATH to point to where all of python protos are located that are not nearby in the filesystem
sys.path.append(str(workspace_path_finder.get_home() / "py_proto"))

# Modify the PATH to point to where the gui_user proto is
sys.path.append(str(workspace_path_finder.find_workspace_path() / "bazel-bin" / "utils" / "gui"))

from proto import gui_user_pb2

gui_user = gui_user_pb2.GuiUser()


def get_root():
    return Tk("main_screen")


def add_text_to_language_selection_frame(frame):
    ttk.Label(frame, text="Select A Language").grid(column=0, row=0)


def add_buttons_to_language_selection_frame(root, frame):
    ttk.Button(frame, txt="Quit", command=root.destroy()).grid(column=1, row=0)

    v = IntVar()
    ttk.Radiobutton(frame, txt="English", command=set_language, value=1, variable=v).grid(column=2, row=0)


def set_language(lang):
    gui_user.language = lang


def get_langauge_selection_frame(root):
    frame = ttk.Frame(root, padding=10)

    add_text_to_language_selection_frame(frame)

    add_buttons_to_language_selection_frame(root, frame)

    return frame


def main():
    root = get_root()

    lang_selection_frame = get_langauge_selection_frame(root)

    root.mainloop()


if __name__ == "__main__":
    main()
