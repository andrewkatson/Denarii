# Configures some of the install files for Denarii.
# This assumes that Denarii has been cloned into your %HOMEDRIVE%%HOMEPATH% repository.
# To see what that is try 'printenv HOMEDRIVE' and 'printenve HOMEPATH'
# This is only for windows

import os
import pathlib
import shutil
import traceback

import common
import workspace_path_finder


class LibraryInfo:

    def __init__(self, libname, foldername="", get_includes=True):
        self.libname = libname
        self.foldername = foldername
        self.folderpath = ""
        self.relevant_paths = []
        self.get_includes = get_includes


# windows only uses the bare number of libraries needed to get everything to build...
win_library_info = [LibraryInfo("liblzma", "liblzma"), LibraryInfo("libsodium", "libsodium"),
                    LibraryInfo("libreadline", "libreadline"), LibraryInfo(
                        "libhidapi", "libhidapi"),
                    LibraryInfo("libusb", "libusb"), LibraryInfo(
                        "libunbound", "libunbound"), LibraryInfo(
                        "libzmq", "libzmq"),
                    LibraryInfo("liblmdb", "db_drivers", False),
                    LibraryInfo("libunwind", "libunwind", False)]

workspace_path = workspace_path_finder.find_workspace_path()


def get_libunwind():
    libunwind_path = workspace_path / "external" / "libunwind"

    if common.check_exists_with_existing_artifact_check(libunwind_path, root_path=libunwind_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting libunwind")

    # libunwind wants to be special so we need to download its source files first
    raw_path = str(workspace_path / "external")

    common.chdir(raw_path)

    clone_command = "git clone git@github.com:llvm-mirror/libunwind.git"
    common.system(clone_command)

    # need to modify the libunwind.h we are using
    source = str(workspace_path) + "/libunwind.h"
    dest = raw_path + "/libunwind/include/libunwind.h"

    move_command = "move " + source + " " + dest
    common.system(move_command)

    # Need to modify an include of libunwind to use "" instead of <>
    # opening the file in read mode
    file = open(dest, "r")
    replacement = ""
    # using the for loop
    for line in file:
        line = line.strip()
        changes = line.replace("<__libunwind_config.h>",
                               "\"__libunwind_config.h\"")
        replacement = replacement + changes + "\n"

    file.close()
    # opening the file in write mode
    fout = open(dest, "w")
    fout.write(replacement)
    fout.close()

    common.check_exists(libunwind_path)


def get_zlib():
    zlib_path = workspace_path / "external" / "zlib"

    if common.check_exists_with_existing_artifact_check(zlib_path, root_path=zlib_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting Zlib")
    raw_path = str(workspace_path / "external")

    common.chdir(raw_path)

    clone_command = "git clone git@github.com:madler/zlib.git"
    common.system(clone_command)

    common.check_exists(zlib_path)


def create_build_file_win(libraries):
    external_dir_path = workspace_path / "external"

    common.print_something("Creating BUILD files for Windows libraries")
    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(external_dir_path, build_file_name)

        if not os.path.exists(path):
            with open(path, 'w'):
                pass
        else:
            common.print_something(f"{path} already exists")

        common.check_exists(path)


def create_folder_win(libraries):
    external_dir_path = workspace_path / "external"

    common.print_something("Creating folders for Windows libraries")
    for library in libraries:

        foldername = library.foldername

        path = os.path.join(external_dir_path, foldername)

        if not os.path.exists(path):
            os.makedirs(path)
        else:
            common.print_something(f"{path} already exists")

        library.folderpath = path

        common.check_exists(path)


def get_relevant_paths_win(libraries):
    common.print_something("Getting relevant paths for Windows libraries")
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
                        library.relevant_paths.append(
                            os.path.join(includes_path, directory))
                for file in files:
                    if name in file and file.endswith(".h"):
                        library.relevant_paths.append(
                            os.path.join(includes_path, file))
            for subdir, dirs, files in os.walk(src_path):
                for file in files:
                    if name in file and file.endswith(".a") or file.endswith(".so"):
                        library.relevant_paths.append(
                            os.path.join(src_path, file))


def find_src_files_win(libraries):
    common.print_something("Finding source files for Windows libraries")
    for library in libraries:

        for path in library.relevant_paths:

            if ".a" in path or ".so" in path:

                filename = path.split("\\")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if os.path.exists(path):
                    common.print_something(
                        "Moving: " + path + " to " + library.folderpath)
                    try:
                        if not os.path.exists(new_path):
                            with open(new_path, 'w'):
                                pass
                    except:
                        common.print_something(
                            "weird this shouldnt happen but is ok")

                    if common.check_exists_with_existing_artifact_check(new_path, delete_single_file=True, fail_on_existence=False):
                        continue

                    shutil.copyfile(path, new_path)

                    common.check_exists(new_path)

                else:
                    common.print_something(path + " does not exist")


def copy_file(path, library):
    common.print_something("Copying files for Windows libraries")
    if "include" in path:
        try:
            filename = path.split("\\")[-1]

            new_path_wo_filename = ""
            # openssl requires it be in a directory called openssl
            if "openssl" in library.libname:
                new_path_wo_filename = os.path.join(
                    library.folderpath, "openssl")
            elif "readline" in library.libname:
                new_path_wo_filename = os.path.join(
                    library.folderpath, "readline")
            elif "sodium" in library.libname:
                new_path_wo_filename = os.path.join(
                    library.folderpath, "sodium")
            else:
                new_path_wo_filename = os.path.join(
                    library.folderpath, "include")

            # the path plus include directory might not exist
            if not os.path.exists(new_path_wo_filename):
                os.makedirs(new_path_wo_filename)

            real_new_path = os.path.join(new_path_wo_filename, filename)

            try:
                if not os.path.exists(real_new_path):
                    with open(real_new_path, 'w'):
                        pass
            except Exception as e:
                common.print_something(e)

            if common.check_exists_with_existing_artifact_check(real_new_path, delete_single_file=True, fail_on_existence=False):
                return

            shutil.copyfile(path, real_new_path)

            common.check_exists(real_new_path)
        except Exception as e:
            common.print_something("Could not copy file " + path)
            common.print_something(e)
            common.print_something(traceback.print_exc())
            exit(-1)


def find_includes_win(libraries):
    common.print_something("Finding include files for Windows libraries")
    for library in libraries:

        if library.get_includes:

            for relevant_path in library.relevant_paths:

                paths = common.get_all_files_paths(relevant_path)

                for path in paths:
                    common.print_something(f"Trying to copy path {path}")
                    copy_file(path, library)


def import_dependencies_win():
    common.print_something("Importing dependencies for Windows")
    get_libunwind()
    get_zlib()
    create_folder_win(win_library_info)
    create_build_file_win(win_library_info)
    get_relevant_paths_win(win_library_info)
    find_includes_win(win_library_info)
    find_src_files_win(win_library_info)


def randomx_win(external_dir_path):
    randomx_path = external_dir_path / "randomx"

    build_path = randomx_path / "build"

    randomx_library_path = build_path / "librandomx.a"

    if common.check_exists_with_existing_artifact_check(randomx_library_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Getting randomx")

    common.chdir(randomx_path)

    common.chdir(build_path)
    command = "cmake -DARCH=native -G \"MinGW Makefiles\" .. && mingw32-make"
    common.system(command)

    common.check_exists(randomx_library_path)


def miniupnp_win(external_dir_path):
    root_miniupnp_path = external_dir_path / "miniupnp"
    # we only need to build one of the subdirectories
    miniupnp_path = external_dir_path / "miniupnp" / "miniupnpc"

    miniupnp_library_path = miniupnp_path / "libminiupnpc.a"
    if common.check_exists_with_existing_artifact_check(miniupnp_library_path, root_path=root_miniupnp_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting miniupnp")
    common.chdir(external_dir_path)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone git@github.com:miniupnp/miniupnp.git"
    common.system(clone_command)

    common.chdir(miniupnp_path)

    command = "cmake -G \"MinGW Makefiles\" . && mingw32-make"
    common.system(command)

    common.check_exists(miniupnp_library_path)


def openpgm_win(external_dir_path):
    openpgm_path = external_dir_path / "openpgm"
    inner_path = openpgm_path / "openpgm" / "pgm"
    binary_path = inner_path / "build" / "lib" / \
        "Debug" / "libpgm-v142-mt-gd-5_2_127.lib"

    if common.check_exists_with_existing_artifact_check(binary_path, root_path=openpgm_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting openpgm for Windows")

    common.chdir(external_dir_path)

    clone_command = "git clone git@github.com:steve-o/openpgm.git"
    common.system(clone_command)

    common.chdir(openpgm_path)

    common.chdir(inner_path)

    make_command = "mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && msbuild /nologo /property:Configuration=Debug ALL_BUILD.vcxproj"
    common.system(make_command)

    common.check_exists(binary_path)


def libnorm_win(external_dir_path):
    libnorm_path = external_dir_path / "libnorm"

    binary_path = libnorm_path / "build" / "norm_static.lib"

    if common.check_exists_with_existing_artifact_check(binary_path, root_path=libnorm_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting libnorm for Windows")

    common.chdir(external_dir_path)

    clone_command = "git clone --recurse-submodules git@github.com:USNavalResearchLaboratory/norm.git"
    common.system(clone_command)

    old_path = external_dir_path / "norm"
    rename_command = f"REN {old_path} libnorm"
    common.system(rename_command)

    common.chdir(libnorm_path)

    build_command = f"python waf configure --prefix={libnorm_path} && python waf && python waf install"
    common.system(build_command)

    common.check_exists(binary_path)


def curl_win(external_dir_path):
    raw_path = external_dir_path / "curl"

    curl_path = raw_path / "curl"

    common.chdir(raw_path)

    if common.check_exists_with_existing_artifact_check(raw_path, root_path=raw_path, delete_tree=True, fail_on_existence=False):
        return

    clone_command = "git clone git@github.com:curl/curl.git"
    os.system(clone_command)

    common.chdir(curl_path)

    command = "buildconf && mingw32-make mingw32"
    os.system(command)

    common.check_exists(curl_path)


def build_dependencies_win():
    external_dir_path = workspace_path / "external"
    randomx_win(external_dir_path)

    miniupnp_win(external_dir_path)

    openpgm_win(external_dir_path)

    libnorm_win(external_dir_path)

    curl_win(external_dir_path)


common.print_something(workspace_path)

import_dependencies_win()

build_dependencies_win()
