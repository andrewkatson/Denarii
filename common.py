# Common functions used in configuration code
import os
import re
import shutil

from difflib import SequenceMatcher

import flags

def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)


def print_something(text):
    print(f"\n\n{text}\n\n")


def system(command):
    print_something(f"Running command {command}")

    os.system(command)


def check_exists(path, fail_on_existence=True):
    if os.path.exists(path):
        print_something(f"Path: {path} exists")
        return True
    else:
        if fail_on_existence:
            print_something(f"Failing because {path} does not exist")
            exit(-1)        
        else:
            print_something(f"Returning false because {path} does not exist")
            return False
        
def check_exists_with_existing_artifact_check(path="", paths=None, root_path="", delete_tree=False, delete_single_file=False, fail_on_existence=True):


    if root_path == "" and delete_tree == True: 
        raise ValueError("If delete_tree is specified you need to supply a root_path")

    if paths is None and path != "": 
        paths = [path]
    elif paths is not None: 
        paths = paths 
    else: 
        raise ValueError(f"Something is wrong with {paths} or {path}")

    all_exist = True
    for some_path in paths: 
        all_exist = check_exists(some_path, fail_on_existence=fail_on_existence) and all_exist 

    if all_exist and flags.args.existing_artifact_delete_policy == flags.SKIP:
        print_something(f"{paths} all already exist")
        # If we want to skip we should exit whatever called this
        return True
    elif all_exist and flags.args.existing_artifact_delete_policy == flags.DELETE:
        if delete_tree: 
            print_something(f"{paths} exist and their tree from {root_path} is going to be deleted")
            shutil.rmtree(root_path)
        if delete_single_file: 
            for some_path in paths:
                print_something(f"{some_path} exists and is going to be deleted")
                os.remove(path)
        # If we delete we want to download them again so dont exit whatever called this
        return False
    elif root_path != "" and os.path.exists(root_path) and delete_tree is True: 
        print_something(f"{paths} does not exist but their tree from {root_path} does so that is going to be deleted")
        shutil.rmtree(root_path)
        # If we delete we want to download them again so dont exit whatever called this
        return False
        
    # If we fall through we allow whatever logic to continue.
    print_something(f"{paths} do not exist and we are going to allow them to be created")
    return False
        

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