# Common functions used in configuration code
import os
import re
import shutil

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
        
def check_exists_with_existing_artifact_check(path, delete_tree=False, delete_single_file=False, fail_on_existence=True):
    exists = common.check_exists(new_path, fail_on_existence=fail_on_existence) 
    if exists and flags.args.existing_artifact_delete_policy == flags.SKIP:
        common.print_something(f"{new_path} already exists")
        # If we want to skip we should exit whatever called this
        return True
    elif exists and flags.args.existing_artifact_delete_policy == flags.DELETE:
        common.print_something(f"{new_path} exists and is going to be deleted")
        if delete_tree: 
            shutil.rmtree(new_path)
        if delete_single_file: 
            os.remove(new_path)
        # If we delete we want to download them again so dont exit whatever called this
        return False
            
    # To be safe we do nothing.
    return True
            

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