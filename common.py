# Common functions used in configuration code
import os
import re

from difflib import SequenceMatcher


def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)


def print_something(text):
    print(f"\n\n{text}\n\n")


def system(command):
    print_something(f"Running command {command}")

    os.system(command)


def check_exists(path):
    if os.path.exists(path):
        print_something(f"Path: {path} exists")
    else:
        print_something(f"Path {path} does not exist failing")
        exit(-1)


def get_all_files_paths(path):
    paths = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            paths.append(os.path.join(subdir, file))

        for dir in dirs:
            new_paths = get_all_files_paths(dir)
            for new_path in new_paths:
                paths.append(new_path)

    return paths


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def replace_phrase(phrase_to_replace, replace_with, path):

    new_file = ""

    with open (path, 'r', encoding='latin-1') as f:
        content = f.read()
        content_new = re.sub(phrase_to_replace, replace_with, content, flags = re.M)
        new_file += f"{content_new} \n"

    with open(path, 'w', encoding='latin-1') as f:
        f.write(new_file)