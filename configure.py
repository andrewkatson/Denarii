# Configures some of the install files for denarii.
# This assumes that denarii has been cloned into your $HOME repository.
# To see what that is try 'printenv HOME'

import os
import pathlib
import shutil
import subprocess


class LibraryInfo:

    def __init__(self, libname, foldername):
        self.libname = libname
        self.foldername = foldername
        self.folderpath = ""
        self.relevant_paths = []

# note doxygen and graphviz do not work properly
library_info = [LibraryInfo("libnorm-dev", "libnorm"), LibraryInfo("libunbound-dev", "libunbound"),
                LibraryInfo("libpgm-dev", "openpgm"),
                LibraryInfo("libsodium-dev", "libsodium"), LibraryInfo("libunwind-dev", "libunwind"),
                LibraryInfo("liblzma-dev", "liblzma"),
                LibraryInfo("libreadline-dev", "libreadline"), LibraryInfo("libldns-dev", "ldns"),
                LibraryInfo("libexpat1-dev", "expat"),
                LibraryInfo("doxygen", "doxygen"), LibraryInfo("qttools5-dev-tools", "lrelease"),
                LibraryInfo("graphviz", "graphviz"),
                LibraryInfo("libhidapi-dev", "libhidapi"), LibraryInfo("libusb-1.0-0-dev", "libusb"),
                LibraryInfo("libudev-dev", "libudev")]

# NEED TO FILL THIS IN WITH YOUR USERNAME FOR THIS TO WORK SORRY
username = "andrew"
dirpath = os.path.join("/home/" + username, "denarii/external")


def create_build_file(libraries):
    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(dirpath, build_file_name)

        if not os.path.exists(path):
            os.mknod(path)


def create_folder(libraries):
    for library in libraries:

        foldername = library.foldername

        path = os.path.join(dirpath, foldername)

        if not os.path.exists(path):
            os.makedirs(path)

        library.folderpath = path


def get_relevant_paths(libraries):
    for library in libraries:
        files = subprocess.check_output(["dpkg", "-L", library.libname])

        file_as_str = str(files)

        # need to split along usr because the paths are all concatenated
        broken_up = file_as_str.split("usr")

        for broken in broken_up:
            fixed = "/usr" + broken
            # all these strings end with /n\ so we need to peel it off
            fixed = fixed[:-3]
            if not os.path.exists(fixed):
                # if there is still something wrong with the path we try to fix it
                # usually there are just weird escape characters in it
                fixed = fixed.replace(R"\n", "")

            if not os.path.exists(fixed):
                # a special case where libudev is installed in /lib instead of a /usr directory
                if "/lib" in fixed:
                    fixed = fixed.split("/lib/")
                    fixed = "/lib/" + fixed[1]
            library.relevant_paths.append(fixed)


def find_src_files(libraries):
    for library in libraries:

        for path in library.relevant_paths:

            if ".a" in path or ".so" in path:

                filename = path.split("/")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if os.path.exists(path):
                    print("Moving: " + path + " to " + library.folderpath)
                    try:
                        if not os.path.exists(new_path):
                            os.mknod(new_path)
                    except:
                        print("weird this shouldnt happen but is ok")
                    finally:
                        print(" ALREADY EXISTS " + new_path)
                    shutil.copyfile(path, new_path)
                else:
                    print(path + " does not exist")


def find_includes(libraries):

    for library in libraries:

        for path in library.relevant_paths:

            if "include" in path:
                try:
                    filename = path.split("/")[-1]
                    new_path = os.path.join(library.folderpath + "/include", filename)

                    new_path_wo_filename = os.path.join(library.folderpath + "/include")

                    # the path plus include directory might not exist
                    if not os.path.exists(new_path_wo_filename):
                        os.makedirs(new_path_wo_filename)

                    try:
                        if not os.path.exists(new_path):
                            os.mknod(new_path)
                    except Exception as e:
                        print("ALREADY EXISTS " + new_path)

                    shutil.copyfile(path, new_path)
                except Exception as e:
                    print("Could not copy file " + path)
                    print(e)

create_folder(library_info)
create_build_file(library_info)
get_relevant_paths(library_info)
find_includes(library_info)
find_src_files(library_info)
