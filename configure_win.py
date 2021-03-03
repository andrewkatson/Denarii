# Configures some of the install files for denarii.
# This assumes that denarii has been cloned into your $HOME repository.
# To see what that is try 'printenv HOME'
# This is only for windows

import argparse
import glob
import os
import pathlib
import platform
import re
import requests
import shutil
import subprocess
import sys
import zipfile


class LibraryInfo:

    def __init__(self, libname, foldername="", get_includes=True):
        self.libname = libname
        self.foldername = foldername
        self.folderpath = ""
        self.relevant_paths = []
        self.get_includes = get_includes


# windows only uses the bare number of libraries needed to get everything to build...
win_library_info = [LibraryInfo("liblzma", "liblzma"), LibraryInfo("libsodium", "libsodium"),
                    LibraryInfo("libreadline", "libreadline"), LibraryInfo("libhidapi", "libhidapi"),
                    LibraryInfo("libusb", "libusb"), LibraryInfo("libunbound", "unbound"),
                    LibraryInfo("libopenssl", "openssl"), LibraryInfo("libzmq", "libzmq"),
                    LibraryInfo("zlib", "zlib"), LibraryInfo("liblmdb", "db_drivers", False),
                    LibraryInfo("libunwind", "libunwind", False)]

parser = argparse.ArgumentParser(description="Process command line flags")
parser.add_argument('--workspace_path', type=str, help='The path to the relevant WORKSPACE file', default='')

args = parser.parse_args()

workspace_path = pathlib.Path()


def find_workspace_path():
    global workspace_path

    if args.workspace_path == '':
        # Need to explicitly set this or pass it in as a variable.
        linux_workspace_path = pathlib.Path("/home/andrew/denarii")
        windows_workspace_path = pathlib.Path("C:/Users/katso/Documents/Github/denarii")

        # A workspace path that works if not sudo on EC2
        try:
            possible_workspace_path = os.environ["HOME"] + "/denarii"
            if os.path.exists(possible_workspace_path):
                workspace_path = possible_workspace_path
        except Exception as e:
            print(e)
            print("The HOME variable does not point to the directory")

        # A workspace path that works in sudo on EC2
        try:
            possible_workspace_path = "home/" + os.environ["SUDO_USER"] + "/denarii"

            if os.path.exists(possible_workspace_path):
                workspace_path = possible_workspace_path
        except Exception as e:
            print(e)
            print("Not on an EC2 using sudo")

        if os.path.exists(linux_workspace_path):
            workspace_path = linux_workspace_path
        elif os.path.exists(windows_workspace_path):
            workspace_path = windows_workspace_path
    else:
        workspace_path = args.workspace_path


def get_libunwind():
    # libunwind wants to be special so we need to download its source files first
    raw_path = str(workspace_path / "external")

    os.chdir(raw_path)

    clone_command = "git clone https://github.com/libunwind/libunwind.git"
    os.system(clone_command)


def create_build_file_win(libraries):
    external_dir_path = workspace_path / "external"

    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(external_dir_path, build_file_name)

        if not os.path.exists(path):
            with open(path, 'w'):
                pass


def create_folder_win(libraries):
    external_dir_path = workspace_path / "external"

    for library in libraries:

        foldername = library.foldername

        path = os.path.join(external_dir_path, foldername)

        if not os.path.exists(path):
            os.makedirs(path)

        library.folderpath = path


def get_relevant_paths_win(libraries):
    base_path = pathlib.Path(R"C:\msys64\mingw64")
    includes_path = os.path.join(base_path, "include")
    src_path = os.path.join(base_path, "lib")

    for library in libraries:
        names = [library.libname]

        # zlib has weird files we can just include the path to
        if "zlib" in names:
            library.relevant_paths.append(str(base_path / "lib/libz.a"))
            continue

        names = [name.replace("lib", "") for name in names]

        # openssl has .a files that go by different names
        if "openssl" in names:
            names = ["openssl", "libssl", "libcrypto"]

        for name in names:
            for subdir, dirs, files in os.walk(includes_path):
                for directory in dirs:
                    if name in directory:
                        library.relevant_paths.append(os.path.join(includes_path, directory))
                        break
                for file in files:
                    if name in file and file.endswith(".h"):
                        library.relevant_paths.append(os.path.join(includes_path, file))
                        break
            for subdir, dirs, files in os.walk(src_path):
                for file in files:
                    if name in file and file.endswith(".a"):
                        library.relevant_paths.append(os.path.join(src_path, file))
                        break


def find_src_files_win(libraries):
    for library in libraries:

        for path in library.relevant_paths:

            if ".a" in path or ".so" in path:

                filename = path.split("\\")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if os.path.exists(path):
                    print("Moving: " + path + " to " + library.folderpath)
                    try:
                        if not os.path.exists(new_path):
                            with open(new_path, 'w'):
                                pass
                    except:
                        print("weird this shouldnt happen but is ok")
                    finally:
                        print(" ALREADY EXISTS " + new_path)
                    shutil.copyfile(path, new_path)

                else:
                    print(path + " does not exist")


def copy_file(path, library):
    if "include" in path:
        try:
            filename = path.split("\\")[-1]
            new_path = os.path.join(library.folderpath + "/include", filename)

            new_path_wo_filename = os.path.join(library.folderpath + "/include")

            # the path plus include directory might not exist
            if not os.path.exists(new_path_wo_filename):
                os.makedirs(new_path_wo_filename)

            try:
                if not os.path.exists(new_path):
                    with open(new_path, 'w'):
                        pass
            except Exception as e:
                print("ALREADY EXISTS " + new_path)

            shutil.copyfile(path, new_path)
        except Exception as e:
            print("Could not copy file " + path)
            print(e)


def find_includes_win(libraries):
    for library in libraries:

        if library.get_includes:

            for path in library.relevant_paths:

                if os.path.isdir(path):
                    for subdir, dirs, files in os.walk(path):
                        for file in files:
                            full_path = os.path.join(path, file)
                            copy_file(full_path, library)
                else:
                    copy_file(path, library)


def import_dependencies_win():
    get_libunwind()
    create_folder_win(win_library_info)
    create_build_file_win(win_library_info)
    get_relevant_paths_win(win_library_info)
    find_includes_win(win_library_info)
    find_src_files_win(win_library_info)


find_workspace_path()

import_dependencies_win()
