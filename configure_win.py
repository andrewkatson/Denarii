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
import workspace_path_finder
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
                    LibraryInfo("liblmdb", "db_drivers", False),
                    LibraryInfo("libunwind", "libunwind", False)]

workspace_path = pathlib.Path()


def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)


def get_libunwind():
    # libunwind wants to be special so we need to download its source files first
    raw_path = str(workspace_path / "external")

    chdir(raw_path)

    clone_command = "git clone https://github.com/llvm-mirror/libunwind.git"
    os.system(clone_command)

    # need to modify the libunwind.h we are using
    source = str(workspace_path) + "/libunwind.h"
    dest = raw_path + "/libunwind/include/libunwind.h"

    move_command = "move " + source + " " + dest
    os.system(move_command)


def get_zlib():
    raw_path = str(workspace_path / "external")

    chdir(raw_path)

    clone_command = "git clone git@github.com:andrewkatson/zlib.git"
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

            new_path_wo_filename = ""
            # openssl requires it be in a directory called openssl
            if "openssl" in library.libname:
                new_path_wo_filename = os.path.join(library.folderpath, "openssl")
            elif "readline" in library.libname:
                new_path_wo_filename = os.path.join(library.folderpath, "readline")
            elif "sodium" in library.libname:
                new_path_wo_filename = os.path.join(library.folderpath, "sodium")
            else:
                new_path_wo_filename = os.path.join(library.folderpath, "include")

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
    get_zlib()
    create_folder_win(win_library_info)
    create_build_file_win(win_library_info)
    get_relevant_paths_win(win_library_info)
    find_includes_win(win_library_info)
    find_src_files_win(win_library_info)


def randomx_win(external_dir_path):
    raw_path = str(external_dir_path)

    randomx_path = raw_path + "/randomx"

    chdir(randomx_path)

    build_path = randomx_path + "/build"
    chdir(build_path)
    command = "cmake -DARCH=native -G \"MinGW Makefiles\" .. && mingw32-make"
    os.system(command)


workspace_path = workspace_path_finder.find_workspace_path()
print(workspace_path)
import_dependencies_win()

external_dir_path = workspace_path / "external"
randomx_win(external_dir_path)
