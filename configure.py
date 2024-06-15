# Configures some of the install files for Denarii.
# This assumes that Denarii has been cloned into your $HOME repository. Or on Windows your %HOMEDRIVE%%HOMEPATH%
# To see what that is try 'printenv HOME' or 'printenv HOMEDRIVE' and 'printenv HOMEPATH'

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

import common
import workspace_path_finder

workspace_path = workspace_path_finder.find_workspace_path()

py_pb_files_to_check = ["any_pb2.py", "api_pb2.py", "descriptor_pb2.py", "duration_pb2.py", "empty_pb2.py",
                        "field_mask_pb2.py", "source_context_pb2.py", "struct_pb2.py", "timestamp_pb2.py",
                        "type_pb2.py",
                        "wrappers_pb2.py"]

py_files_to_check = ["descriptor.py", "descriptor_pool.py",
                     "message.py", "reflection.py", "symbol_database.py"]

common_bazel_options_windows = f' --output_base="C:\\bazel-bin '
common_bazel_build_command_options_windows = f' --extra_toolchains=@local_config_cc//:cc-toolchain-x64_windows_mingw --extra_execution_platforms=//:windows-mingw-gcc '
common_build_options_windows = f' --compiler=mingw-gcc --host_compiler=mingw-gcc --copt="-O3" --copt="-DWIN32_LEAN_AND_MEAN" ' \
                               '--copt="-DMINIUPNP_STATICLIB" --copt="-DZMQ_STATIC" --linkopt="-static" '


class LibraryInfo:

    def __init__(self, libname, foldername=""):
        # The name given to the library by the system on Linux.
        # This is the name given when downloading on Linux.
        # It is used to keep the files in a named location.
        # On Mac this is just the Linux name because we want the files
        # to be stored in the same named folders.
        self.libname = libname
        # The name of the folder on the harddrive where the files are located.
        self.foldername = foldername
        # The path to the folder where the files for this are stored.
        self.folderpath = ""
        # The paths to lib, bin, and include directories for the files for the library.
        self.relevant_paths = []


# note doxygen and graphviz do not work properly
linux_library_info = [LibraryInfo("libnorm-dev", "libnorm"), LibraryInfo("libunbound-dev", "libunbound"),
                      LibraryInfo("libpgm-dev", "openpgm"),
                      LibraryInfo(
                          "libsodium-dev", "libsodium"), LibraryInfo("libunwind-dev", "libunwind"),
                      LibraryInfo("liblzma-dev", "liblzma"),
                      LibraryInfo(
                          "libreadline-dev", "libreadline"), LibraryInfo("libldns-dev", "ldns"),
                      LibraryInfo("libexpat1-dev", "expat"),
                      LibraryInfo("doxygen", "doxygen"), LibraryInfo(
                          "qttools5-dev-tools", "lrelease"),
                      LibraryInfo("graphviz", "graphviz"),
                      LibraryInfo(
                          "libhidapi-dev", "libhidapi"), LibraryInfo("libusb-1.0-0-dev", "libusb"),
                      LibraryInfo("libudev-dev", "libudev")]

mac_library_info = [LibraryInfo("autoconf"), LibraryInfo("autogen"), LibraryInfo("automake"), LibraryInfo("coreutils"),
                    LibraryInfo("pkg-config"), LibraryInfo(
                        "openssl"), LibraryInfo("hidapi", "libhidapi"), LibraryInfo("zmq", "libzmq"), LibraryInfo("libpgm", "openpgm"),
                    LibraryInfo("unbound", "libunbound"), LibraryInfo("libsodium"), LibraryInfo(
                        "miniupnpc", "miniupnp"), LibraryInfo("readline", "libreadline"), LibraryInfo("ldns"), LibraryInfo("expat"),
                    LibraryInfo("doxygen"), LibraryInfo("graphviz"), LibraryInfo("libunwind-headers", "libunwind"), LibraryInfo("xz", "liblzma"), LibraryInfo("protobuf")]


github_path = workspace_path.parent
print(f"GITHUB PATH {github_path}")


def download_url(url, save_path, chunk_size=128):
    common.print_something(f"Downloading url {url} to {save_path}")
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def create_build_file(libraries):
    common.print_something("Creating BUILD files for libraries")
    external_dir_path = workspace_path / "external"

    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(external_dir_path, build_file_name)

        if not os.path.exists(path):
            os.mknod(path)
        else:
            common.print_something(f"{path} already exists")

        common.check_exists(path)


def create_folder(libraries):
    common.print_something("Creating folders for libraries")
    external_dir_path = workspace_path / "external"

    for library in libraries:

        foldername = ""
        if library.foldername != "":
            foldername = library.foldername
        else:
            foldername = library.libname

        path = os.path.join(external_dir_path, foldername)

        if not os.path.exists(path):
            os.makedirs(path)
        else:
            common.print_something(f"{path} already exists")


        library.folderpath = path

        common.check_exists(path)


def get_relevant_paths(libraries):
    common.print_something("Getting relevant paths for libraries")
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
    common.print_something("Finding source files for libraries")
    for library in libraries:

        for path in library.relevant_paths:

            if ".a" in str(path) or ".so" in str(path):

                filename = path.split("/")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if os.path.exists(path):
                    common.print_something(
                        "Moving: " + path + " to " + library.folderpath)
                    try:
                        if not os.path.exists(new_path):
                            os.mknod(new_path)
                    except Exception as e:
                        common.print_something(e)

                    if common.check_exists_with_existing_artifact_check(new_path, delete_single_file=True, fail_on_existence=False):
                        continue

                    shutil.copyfile(path, new_path)

                    common.check_exists(new_path)
                else:
                    common.print_something(path + " does not exist")


def find_includes(libraries):
    common.print_something("Finding includes for libraries")
    for library in libraries:

        for path in library.relevant_paths:

            if "include" in str(path):
                try:
                    filename = path.split("/")[-1]
                    new_path = os.path.join(
                        library.folderpath + "/include", filename)

                    new_path_wo_filename = os.path.join(
                        library.folderpath + "/include")

                    # the path plus include directory might not exist
                    if not os.path.exists(new_path_wo_filename):
                        os.makedirs(new_path_wo_filename)

                    try:
                        if not os.path.exists(new_path):
                            os.mknod(new_path)
                    except Exception as e:
                        common.print_something(e)

                    if common.check_exists_with_existing_artifact_check(new_path, delete_single_file=True, fail_on_existence=False):
                        continue

                    shutil.copyfile(path, new_path)

                    common.check_exists(new_path)
                except Exception as e:
                    common.print_something(e)
                    exit(-1)


def import_dependencies():
    common.print_something("Importing dependencies")
    create_folder(linux_library_info)
    create_build_file(linux_library_info)
    get_relevant_paths(linux_library_info)
    find_includes(linux_library_info)
    find_src_files(linux_library_info)


def get_relevant_paths_mac(libraries):
    common.print_something("Getting relevant paths for libraries for Mac")
    # All files are located in /opt/homebrew/opt
    base_path = pathlib.Path("/opt/homebrew/opt")

    for library in libraries:

        path = base_path / library.libname

        lib_path = path / "lib"
        bin_path = path / "bin"
        include_path = path / "include"

        # We handle binaries differently from includes because we want to
        # grab every include file in the include diretory and maintain
        # the directory structure. Whereas, we just want the binary file itself
        # from the lib directory.
        for new_path in common.get_all_files_paths(lib_path):
            library.relevant_paths.append(new_path)

        # In case there are any libraries hiding in the bin folder search that
        # too.
        for new_path in common.get_all_files_paths(bin_path):
            library.relevant_paths.append(new_path)

        if os.path.exists(include_path):
            library.relevant_paths.append(include_path)


def find_includes_mac(libraries):
    common.print_something("Finding includes for libraries")

    for library in libraries:

        for path in library.relevant_paths:

            if "include" in str(path):

                try:
                    include_path = pathlib.Path(library.folderpath) / "include"

                    if common.check_exists_with_existing_artifact_check(path=include_path, delete_single_file=True, fail_on_existence=False):
                        continue

                    shutil.copytree(path, include_path)

                except Exception as e:
                    common.print_something(e)

                common.check_exists(include_path)


def find_src_files_mac(libraries):
    common.print_something("Finding source files for libraries for Mac")
    for library in libraries:

        for path in library.relevant_paths:

            if ".a" in str(path) or ".so" in str(path) or ".dylib" in str(path):

                filename = path.split("/")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if common.check_exists_with_existing_artifact_check(path=new_path, delete_single_file=True, fail_on_existence=False):
                    continue

                try:
                    shutil.copyfile(path, new_path)
                except Exception as e:
                    common.print_something(e)

                common.check_exists(new_path)


def import_dependencies_mac():
    common.print_something("Importing dependencies for Mac")
    create_folder(mac_library_info)
    get_relevant_paths_mac(mac_library_info)
    find_includes_mac(mac_library_info)
    find_src_files_mac(mac_library_info)


def spdlog(external_dir_path):
    spdlog_path = external_dir_path / "spdlog"

    spdlog_library_path = spdlog_path / "build" / "libspdlog.a"

    if common.check_exists_with_existing_artifact_check(path=spdlog_library_path, root_path=spdlog_path, fail_on_existence=False):
        return

    common.print_something("Getting spdlog")
    common.chdir(external_dir_path)

    clone_command = "git clone git@github.com:gabime/spdlog.git"
    common.system(clone_command)

    common.chdir(spdlog_path)

    command = "mkdir build && cd build && cmake .. && make -j"
    common.system(command)

    common.check_exists(spdlog_library_path)


def miniupnp(external_dir_path):
    # we only need to build one of the subdirectories but we need to remove the whole tree
    root_miniupnp_path = external_dir_path / "miniupnp"
    miniupnp_path = external_dir_path / "miniupnp" / "miniupnpc"
    miniupnp_library_path = miniupnp_path / "build" / "libminiupnpc.a"

    if common.check_exists_with_existing_artifact_check(path=miniupnp_library_path, root_path=root_miniupnp_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting miniupnp")
    common.chdir(external_dir_path)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone git@github.com:miniupnp/miniupnp.git"
    common.system(clone_command)

    common.chdir(miniupnp_path)

    command = "sudo make install"
    common.system(command)

    common.check_exists(miniupnp_library_path)


def randomx(external_dir_path):
    randomx_path = external_dir_path / "randomx"

    randomx_library_path = randomx_path / "build" / "librandomx.a"

    if common.check_exists_with_existing_artifact_check(path=randomx_library_path, root_path=randomx_path, fail_on_existence=False):
        return

    common.print_something("Getting randomx")
    common.chdir(external_dir_path)

    common.chdir(randomx_path)

    command = "mkdir build && cd build && cmake -DARCH=native .. && make"
    common.system(command)

    common.check_exists(randomx_library_path)


def supercop(external_dir_path):
    supercop_path = external_dir_path / "supercop"

    supercop_64_library_path = supercop_path / "libmonero-crypto64.a"
    supercop_other_library_path = supercop_path / "libmonero-crypto.a"

    if common.check_exists_with_existing_artifact_check(paths=[supercop_64_library_path, supercop_other_library_path], root_path=supercop_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting supercop")

    common.chdir(external_dir_path)

    clone_command = "git clone --recursive git@github.com:andrewkatson/supercop.git && cd supercop && git " \
                    "submodule init && git submodule update "
    common.system(clone_command)

    common.chdir(supercop_path)

    # need to create the first crypto library
    first_create_command = "cmake . && make && sudo make install"
    common.system(first_create_command)

    lib_crypto_path = "/usr/local/lib/libmonero-crypto.a"

    try:
        shutil.copyfile(lib_crypto_path, str(
            supercop_path / "libmonero-crypto64.a"))
    except Exception as e:
        common.print_something(e)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && sudo make install"
    common.system(second_create_command)

    try:
        shutil.copyfile(lib_crypto_path, str(
            supercop_path / "libmonero-crypto.a"))
    except Exception as e:
        common.print_something(e)

    common.check_exists(supercop_64_library_path)
    common.check_exists(supercop_other_library_path)


def unbound(external_dir_path):
    unbound_path = external_dir_path / "unbound"

    libunbound_library_path = unbound_path / "libunbound.so"

    if common.check_exists_with_existing_artifact_check(path=libunbound_library_path, root_path=unbound_path, fail_on_existence=False):
        return

    common.print_something("Getting unbound")
    common.chdir(external_dir_path)

    common.chdir(unbound_path)

    command = "./configure && make && sudo make install"
    common.system(command)

    shutil.copyfile("/usr/local/lib/libunbound.so",
                    str(unbound_path / "libunbound.so"))

    common.check_exists(libunbound_library_path)


def openssl(external_dir_path):
    openssl_path = workspace_path / "external" / "openssl"

    libssl_path = openssl_path / "libssl.a"
    libcrypto_path = openssl_path / "libcrypto.a"

    if common.check_exists_with_existing_artifact_check(paths=[libssl_path, libcrypto_path], root_path=openssl_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting openssl")

    common.chdir(external_dir_path)

    openssl_zip_path = external_dir_path / "openssl.zip"
    download_url(
        "https://www.openssl.org/source/openssl-3.2.1.tar.gz", str(openssl_zip_path))

    unzip_command = "tar -xvzf " + \
        str(openssl_zip_path) + " -C " + str(external_dir_path)
    common.system(unzip_command)

    openssl_wrong_name_path = external_dir_path / "openssl-3.2.1"

    shutil.copytree(str(openssl_wrong_name_path), str(openssl_path))

    common.chdir(openssl_path)

    make_command = "./Configure && make && make test"
    common.system(make_command)

    common.check_exists(libssl_path)
    common.check_exists(libcrypto_path)


def libzmq(external_dir_path):
    libzmq_path = external_dir_path / "libzmq"

    libzmq_library_path = libzmq_path / "libzmq.a"

    if common.check_exists_with_existing_artifact_check(path=libzmq_library_path, root_path=libzmq_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting libzmq")
    common.chdir(external_dir_path)

    clone_command = "git clone git@github.com:zeromq/libzmq.git"
    common.system(clone_command)

    common.chdir(libzmq_path)

    make_command = "./autogen.sh && ./configure --with-libsodium && make && sudo make install"
    common.system(make_command)

    shutil.copyfile("/usr/local/lib/libzmq.a", str(libzmq_library_path))

    common.check_exists(libzmq_library_path)


def zlib(external_dir_path):
    zlib_path = external_dir_path / "zlib"

    if common.check_exists_with_existing_artifact_check(path=zlib_path, root_path=zlib_path, fail_on_existence=False):
        return

    common.print_something("Getting zlib")
    common.chdir(external_dir_path)

    clone_command = "git clone git@github.com:madler/zlib.git"
    common.system(clone_command)

    # We dont check for the existence of a library because zlib is just a normal bazel cc_library
    common.check_exists(zlib_path)

    # We need to add a bit to the top of the zlib file
    gzguts_path = zlib_path / "gzguts.h"
    to_replace_path = workspace_path / "top_of_gzguts.txt"
    replace_with_path = workspace_path / "prepend_to_gzguts.txt"
    with open(to_replace_path, 'r') as to_replace_file:
        to_replace_phrase = to_replace_file.read()
        with open(replace_with_path, 'r') as replace_with_file:
            replace_with_phrase = replace_with_file.read()
            common.replace_phrase(
                to_replace_phrase, replace_with_phrase, gzguts_path)


def liblmdb(external_dir_path):
    liblmdb_path = external_dir_path / "db_drivers" / "liblmdb"

    liblmdb_library_path = liblmdb_path / "liblmdb.a"

    if common.check_exists_with_existing_artifact_check(path=liblmdb_library_path, root_path=liblmdb_path, fail_on_existence=False):
        return

    common.print_something("Getting liblmdb")
    common.chdir(external_dir_path)

    common.chdir(liblmdb_path)
    make_command = "make"
    common.system(make_command)

    common.check_exists(liblmdb_library_path)


def bigint(external_dir_path):
    bigint_path = workspace_path / "external" / "bigint"
    common.chdir(external_dir_path)

    if common.check_exists_with_existing_artifact_check(path=bigint_path, root_path=bigint_path, delete_tree=True, fail_on_existence=False):
        return

    clone_command = "git clone git@github.com:kasparsklavins/bigint.git"
    os.system(clone_command)

    common.check_exists(bigint_path)


def curl(external_dir_path):
    curl_path = workspace_path / "external" / "curl"
    inside_folder_path = curl_path / "curl"
    common.chdir(curl_path)

    if common.check_exists_with_existing_artifact_check(path=inside_folder_path, root_path=curl_path, delete_tree=True, fail_on_existence=False):
        return

    clone_command = "git clone git@github.com:curl/curl.git"
    os.system(clone_command)

    common.chdir(inside_folder_path)

    make_command = "./buildconf && ./configure && make"
    os.system(make_command)

    common.check_exists(inside_folder_path)


def json(external_dir_path):

    json_path = workspace_path / "external/json"

    if common.check_exists_with_existing_artifact_check(path=json_path, root_path=json_path, delete_tree=True, fail_on_existence=False):
        return

    common.chdir(json_path)

    clone_command = "git clone git@github.com:andrewkatson/json.git"
    os.system(clone_command)

    common.check_exists(json_path)


def build_dependencies():
    common.print_something("Building dependencies")

    external_dir_path = workspace_path / "external"
    common.chdir(external_dir_path)

    miniupnp(external_dir_path)

    common.chdir(external_dir_path)
    randomx(external_dir_path)

    common.chdir(external_dir_path)
    supercop(external_dir_path)

    common.chdir(external_dir_path)
    unbound(external_dir_path)

    common.chdir(external_dir_path)
    openssl(external_dir_path)

    common.chdir(external_dir_path)
    libzmq(external_dir_path)

    common.chdir(external_dir_path)
    zlib(external_dir_path)

    common.chdir(external_dir_path)

    liblmdb(external_dir_path)
    common.chdir(external_dir_path)

    bigint(external_dir_path)
    common.chdir(external_dir_path)

    curl(external_dir_path)
    common.chdir(external_dir_path)

    json(external_dir_path)
    common.chdir(external_dir_path)

    spdlog(external_dir_path)
    common.chdir(external_dir_path)


def supercop_win(external_dir_path):
    supercop_path = external_dir_path / "supercop"

    supercop_64_library_path = supercop_path / "libmonero-crypto64.a"
    supercop_other_library_path = supercop_path / "libmonero-crypto.a"

    if common.check_exists_with_existing_artifact_check(paths=[supercop_64_library_path, supercop_other_library_path], root_path=supercop_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting supercop for Windows")

    common.chdir(external_dir_path)

    clone_command = "git clone --recursive git@github.com:andrewkatson/supercop.git && git submodule init && git submodule update"
    common.system(clone_command)

    common.chdir(supercop_path)

    # need to create the first crypto library
    first_create_command = "cmake . && make && sudo make install"
    common.system(first_create_command)

    lib_crypto_path = "/usr/local/lib/libmonero-crypto.a"

    try:
        shutil.copyfile(lib_crypto_path, str(
            supercop_path / "libmonero-crypto64.a"))
    except Exception as e:
        common.print_something(e)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && sudo make install"
    common.system(second_create_command)

    try:
        shutil.copyfile(lib_crypto_path, str(
            supercop_path / "libmonero-crypto.a"))
    except Exception as e:
        common.print_something(e)

    common.check_exists(supercop_64_library_path)
    common.check_exists(supercop_other_library_path)


def build_zlib(external_dir_path):

    zlib_path = external_dir_path / "zlib"

    common.chdir(zlib_path)

    # Run this everytime there doesn't seem to be any harm
    command = "./configure"
    common.system(command)

    # need to undef UNISTD_H
    zconf_path = zlib_path / "zconf.h"
    common.replace_phrase("#  define Z_HAVE_UNISTD_H",
                          "#  undef Z_HAVE_UNISTD_H", zconf_path)


def build_dependencies_win():
    common.print_something("Building dependencies for Windows")
    external_dir_path = workspace_path / "external"

    # The crypto algorithm libraries cannot be found on cygwin
    if sys.platform != "cygwin":
        common.chdir(external_dir_path)
        supercop_win(external_dir_path)

    build_zlib(external_dir_path)

    common.chdir(external_dir_path)
    bigint(external_dir_path)

    json(external_dir_path)
    common.chdir(external_dir_path)

    spdlog(external_dir_path)
    common.chdir(external_dir_path)


def randomx_mac(external_dir_path):
    randomx_path = external_dir_path / "randomx"

    randomx_library_path = randomx_path / "build" / "librandomx.a"

    build_folder_path = randomx_path / "build"

    if common.check_exists_with_existing_artifact_check(path=randomx_library_path, delete_tree=True, root_path=build_folder_path, fail_on_existence=False):
        return

    common.print_something("Getting randomx")
    common.chdir(external_dir_path)

    common.chdir(randomx_path)

    command = "mkdir build && cd build && cmake -DARCH=native .. && make"
    common.system(command)

    common.check_exists(randomx_library_path)


def liblmdb_mac(external_dir_path):
    liblmdb_path = external_dir_path / "db_drivers" / "liblmdb"

    liblmdb_library_path = liblmdb_path / "liblmdb.a"

    if common.check_exists_with_existing_artifact_check(path=liblmdb_library_path, root_path=liblmdb_path, fail_on_existence=False):
        return

    common.print_something("Getting liblmdb")
    common.chdir(external_dir_path)

    common.chdir(liblmdb_path)
    make_command = "make"
    common.system(make_command)

    common.check_exists(liblmdb_library_path)


def libnorm_mac(external_dir_path):
    libnorm_path = external_dir_path / "libnorm"

    binary_path = libnorm_path / "build" / "libnorm.a"

    if common.check_exists_with_existing_artifact_check(path=binary_path, root_path=libnorm_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting libnorm")
    common.chdir(external_dir_path)

    clone_command = "git clone --recurse-submodules git@github.com:USNavalResearchLaboratory/norm.git"
    common.system(clone_command)

    old_path = external_dir_path / "norm"
    rename_command = f"mv {old_path} {libnorm_path}"
    common.system(rename_command)

    common.chdir(libnorm_path)

    path_to_waf = libnorm_path / "waf"
    # We need libnorm to use python3 since mac doenst play nice with python2 and bazel.
    common.replace_phrase("#!\/usr\/bin\/env python",
                          "#!/usr/bin/env python3", path_to_waf)

    build_command = f"./waf configure --prefix={libnorm_path} && ./waf && ./waf install"
    common.system(build_command)

    common.check_exists(binary_path)
    
    # Delete the recursive symbolic links
    norm_recursive_path = libnorm_path / "norp"/ "norm"
    os.removedirs(norm_recursive_path)


def libusb_mac(external_dir_path):
    libusb_path = external_dir_path / "libusb"

    binary_path = libusb_path / "lib" / "libusb-1.0.a"

    if common.check_exists_with_existing_artifact_check(path=binary_path, root_path=libusb_path, delete_tree=True, fail_on_existence=False):
        return

    common.print_something("Getting libusb")
    common.chdir(external_dir_path)

    clone_command = "git clone git@github.com:libusb/libusb.git"
    common.system(clone_command)

    common.chdir(libusb_path)

    build_command = f"./autogen.sh --prefix={libusb_path} && make && make install"
    common.system(build_command)

    common.check_exists(binary_path)

    libusbi_path = libusb_path / "libusb" / "libusbi.h"
    darwin_usb_path = libusb_path / "libusb" / "os" / "darwin_usb.c"

    # We need to change some files to use quotes instead of angled brackets.
    common.replace_phrase("<config.h>", '"config.h"', libusbi_path)
    common.replace_phrase("<config.h>", '"config.h"', darwin_usb_path)


def build_dependencies_mac():
    common.print_something("Building dependencies for Mac")
    external_dir_path = workspace_path / "external"

    common.chdir(external_dir_path)
    randomx_mac(external_dir_path)

    common.chdir(external_dir_path)
    liblmdb_mac(external_dir_path)

    common.chdir(external_dir_path)
    libnorm_mac(external_dir_path)

    common.chdir(external_dir_path)
    libusb_mac(external_dir_path)

    common.chdir(external_dir_path)
    bigint(external_dir_path)

    common.chdir(external_dir_path)
    curl(external_dir_path)

    common.chdir(external_dir_path)
    json(external_dir_path)

    common.chdir(external_dir_path)
    zlib(external_dir_path)

    spdlog(external_dir_path)
    common.chdir(external_dir_path)


def trezor_common():
    trezor_common_build_file_path = workspace_path / \
        "trezor_common_build_file.txt"

    trezor_dest_build_file_path = workspace_path / \
        "external" / "trezor-common" / "protob" / "BUILD"

    if common.check_exists_with_existing_artifact_check(paths=[trezor_dest_build_file_path], delete_single_file=True, fail_on_existence=False):
        return

    try:
        with open(trezor_common_build_file_path) as f:
            text = f.read()
        common.print_something("Setting up trezor common")

        path_to_dir = str(workspace_path / "external" /
                          "trezor-common" / "protob")
        common.chdir(path_to_dir)

        common.system(f"echo \'{text}\' > BUILD")

    except Exception as e:
        common.print_something(e)

    common.check_exists(trezor_dest_build_file_path)


def blocks_generate():
    common.print_something("Generating blocks files")
    input_files = ["checkpoints.dat",
                   "stagenet_blocks.dat", "testnet_blocks.dat"]
    output_files = ["generated_checkpoints.c",
                    "generated_stagenet_blocks.c", "generated_testnet_blocks.c"]
    base_names = ["checkpoints", "stagenet_blocks", "testnet_blocks"]

    for i in range(len(input_files)):
        input_file = input_files[i]
        output_file = output_files[i]
        base_name = base_names[i]

        path_to_output = workspace_path / "src" / "blocks" / output_file

        if common.check_exists_with_existing_artifact_check(path=path_to_output, delete_single_file=True, fail_on_existence=False):
            continue

        path_to_blocks = str(workspace_path) + "/src/blocks"
        command = "cd " + path_to_blocks + " && echo '#include\t<stddef.h>\n#ifndef _WIN32' > " + output_file \
                  + " && echo 'const\tunsigned\tchar\t" + base_name + "[]={' >> " + output_file + " && od -v -An -tx1 " \
                  + input_file + " | sed -e 's/[0-9a-fA-F]\\{1,\\}/0x&,/g' -e '$s/.$//' >> " + output_file + " && echo '};' >> " + output_file \
                  + " && echo 'const\tsize_t\t" + base_name + \
            "_len\t=\tsizeof(" + base_name + ");\n#endif' >> " + output_file

        common.system(command)

    for output in output_files:
        path_to_output = workspace_path / "src" / "blocks" / output
        common.check_exists(path_to_output)


def crypto_wallet_generate():
    common.print_something("Generating crypto wallet directory")
    crypto_wallet_path = workspace_path / "src" / "crypto" / "wallet"
    ops_file = "ops.h"

    supercop_path = workspace_path / "external" / "supercop"
    copy_file_path = supercop_path / "include" / "monero" / "crypto.h"

    ops_file_path = crypto_wallet_path / ops_file
    if common.check_exists_with_existing_artifact_check(path=ops_file_path, delete_single_file=True, fail_on_existence=False):
        return

    # If we are on Linux and have 64 bit processor we can use monero's default crypto libraries
    if re.match(".*nix.*|.*ux.*", platform.system()) and re.match(".*amd64.*|.*AMD64.*|.*x86_64.*",
                                                                  platform.processor()):

        # copy the contents of the crypto file over to ops
        with open(copy_file_path, "r") as copy:
            # generate the file
            command = "cd " + str(crypto_wallet_path) + \
                " && echo > " + ops_file
            common.system(command)

            # the license causes all sorts of problems with echo so we just skip it
            seen_license_info = False
            for line in copy:
                if "MONERO_CRYPTO_H" in line:
                    seen_license_info = True

                if seen_license_info and "#include \"monero/crypto/amd64-64-24k.h\"" in line:
                    # we have to output a different line than the include in this line because
                    # bazel will not be viewing that dependency in the same way that cmake does
                    modified_line = "#include \"include/monero/crypto/amd64-64-24k.h\""
                    copy_line_command = "cd " + str(crypto_wallet_path) + \
                        " && echo '" + modified_line + "' >> " + ops_file
                    common.system(copy_line_command)

                elif seen_license_info and "#include \"monero/crypto/amd64-51-30k.h\"" in line:
                    # we have to output a different line than the include in this line because
                    # bazel will not be viewing that dependency in the same way that cmake does
                    modified_line = "#include \"include/monero/crypto/amd64-51-30k.h\""
                    copy_line_command = "cd " + str(crypto_wallet_path) + \
                        " && echo '" + modified_line + "' >> " + ops_file
                    common.system(copy_line_command)

                elif seen_license_info:
                    copy_line_command = "cd " + str(crypto_wallet_path) + \
                        " && echo '" + line + "' >> " + ops_file
                    common.system(copy_line_command)
    else:
        # Otherwise create an empty file.
        command = "cd " + str(crypto_wallet_path) + " && touch " + \
            ops_file + " && echo \"#pragma once\" >> " + ops_file
        common.system(command)

    common.check_exists(ops_file_path)


def is_git_repo():
    if subprocess.call(["git", "branch"], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) != 0:
        return False
    else:
        return True


def have_git():
    try:
        # pipe output to /dev/null for silence
        null = open("/dev/null", "w")
        subprocess.Popen("git", stdout=null, stderr=null)
        null.close()
        return True
    except OSError:
        return False


version_re = re.compile('^Version: (.+)$', re.M)


def get_version():
    common.print_something("Getting Git version")
    d = str(workspace_path)

    if os.path.isdir(os.path.join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git rev-parse --short=9 HEAD'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            common.print_something(
                'Unable to get version number from git tags')
            exit(1)

        # PEP 386 compatibility
        if '-' in version:
            version = '.post'.join(version.split('-')[:2])

        # Don't declare a version "dirty" merely because a time stamp has
        # changed. If it is dirty, append a ".dev1" suffix to indicate a
        # development revision after the release.
        with open(os.devnull, 'w') as fd_devnull:
            subprocess.call(['git', 'status'],
                            stdout=fd_devnull, stderr=fd_devnull)

        cmd = 'git diff-index --name-only HEAD'.split()
        try:
            dirty = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            common.print_something('Unable to get git index status')
            exit(1)

        if dirty != '':
            version += '.dev1'

    else:
        # Extract the version from the PKG-INFO file.
        with open(os.path.join(d, 'PKG-INFO')) as f:
            version = version_re.search(f.read()).group(1)

    return version


def generate_version_file_with_replacement(version_tag, is_release):
    common.print_something("Generating version file")
    version_tag_str = "@VERSIONTAG@"
    version_release_str = "@VERSION_IS_RELEASE@"

    input_file = "version.cpp.in"
    output_file = "version.cpp"

    src_directory = workspace_path / "src"

    input_file_path = os.path.join(src_directory, input_file)

    version_file_path = src_directory / output_file

    if common.check_exists_with_existing_artifact_check(path=version_file_path, delete_single_file=True, fail_on_existence=False):
        return

    with open(input_file_path, "r") as copy:

        # create the file
        create_file_command = "cd " + \
            str(src_directory) + " && echo > " + output_file
        common.system(create_file_command)

        for line in copy:
            line_to_write = line
            if version_tag_str in line:
                line_to_write = line.replace(version_tag_str, version_tag)

            if version_release_str in line:
                line_to_write = line.replace(
                    version_release_str, str(is_release).lower())

            write_line_command = "cd " + str(src_directory) + \
                " && echo '" + line_to_write + "' >> " + output_file
            common.system(write_line_command)
    common.check_exists(version_file_path)


def version_generate():
    if have_git():
        version_tag = ""
        is_release = False

        # if we are in a git repo then this is not a release branch
        if is_git_repo():
            version_tag = get_version().split(".")[0]
        else:
            version_tag = "release"
            is_release = True

        generate_version_file_with_replacement(version_tag, is_release)

    else:
        raise Exception("No git version found")


def generate_benchmark_file_with_replacement(replacement):
    common.print_something("Generating benchmark file with replacement")
    benchmark_str = "@MONERO_WALLET_CRYPTO_BENCH_NAMES@"

    input_file = "benchmark.h.in"
    output_file = "benchmark.h"

    tests_directory = workspace_path / "tests"

    input_file_path = tests_directory / input_file

    benchmark_file_path = tests_directory / output_file

    if common.check_exists_with_existing_artifact_check(path=benchmark_file_path, delete_single_file=True, fail_on_existence=False):
        return

    with open(input_file_path, "r") as copy:

        for line in copy:
            line_to_write = line

            if benchmark_str in line:
                line_to_write = line.replace(benchmark_str, replacement)

            write_line_command = "cd " + str(tests_directory) + \
                " && echo '" + line_to_write + "' >> " + output_file
            common.system(write_line_command)

    common.check_exists(benchmark_file_path)


def benchmark_generate():
    replacement = ""

    # If we are on Linux and have 64 bit processor we can use monero's default crypto libraries
    if re.match(".*nix.*|.*ux.*", platform.system()) and re.match(".*amd64.*|.*AMD64.*|.*x86_64.*",
                                                                  platform.processor()):
        replacement = "(cn)(amd64_64_24k)(amd64_51_30k)"
    else:
        replacement = "(cn)"

    generate_benchmark_file_with_replacement(replacement)


def convert_translation_files():
    common.print_something("Conveting translation files")
    translation_file_dir = workspace_path / "translations"

    common.chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        converted_file = converted_files[i]
        translated_file_path = translation_file_dir / converted_file

        if common.check_exists_with_existing_artifact_check(path=translated_file_path, delete_single_file=True, fail_on_existence=False):
            continue

        file = files[i]

        conversion_command = "lrelease " + file + " -qm " + converted_file
        common.system(conversion_command)

        common.check_exists(translated_file_path)

    return converted_files


def convert_translation_files_win():
    common.print_something("Converting translation files for Windows")
    translation_file_dir = workspace_path / "translations"

    common.chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        converted_file = converted_files[i]
        translated_file_path = translation_file_dir / converted_file

        if common.check_exists_with_existing_artifact_check(path=translated_file_path, delete_single_file=True, fail_on_existence=False):
            continue

        file = files[i]

        if sys.platform == "cygwin":
            conversion_command = "/mingw64/bin/lrelease.exe " + file + " -qm " + converted_file
        else:
            conversion_command = "/mingw64/bin/lrelease " + file + " -qm " + converted_file
        common.system(conversion_command)

        common.check_exists(translated_file_path)

    return converted_files


def convert_translation_files_mac():
    common.print_something("Converting translation files for Mac")
    translation_file_dir = workspace_path / "translations"

    common.chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        converted_file = converted_files[i]
        translated_file_path = translation_file_dir / converted_file

        if common.check_exists_with_existing_artifact_check(path=translated_file_path, delete_single_file=True, fail_on_existence=False):
            continue

        file = files[i]

        conversion_command = "/opt/homebrew/opt/qt5/bin/lrelease " + \
            file + " -qm " + converted_file
        common.system(conversion_command)

        common.check_exists(translated_file_path)

    return converted_files


def run_translation_generation(translation_files):
    translation_file_dir = workspace_path / "translations"

    translation_file_path = translation_file_dir / "translation_files.h"

    if common.check_exists_with_existing_artifact_check(path=translation_file_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Running translation generation")
    # create the file first
    create_command = "cd " + \
        str(translation_file_dir) + " && echo > translation_files.h"
    common.system(create_command)

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    common.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = str(
        workspace_path) + "/bazel-bin/translations/generate_translations " + str(translation_file_path) + " "

    for translation_file in translation_files:
        translated_file_path = translation_file_dir / translation_file

        generation_command = generation_command + " " + \
            str(translated_file_path)

        common.system(generation_command)

    common.check_exists(translation_file_path)


def run_translation_generation_win(translation_files):
    translation_file_dir = workspace_path / "translations"

    translation_file_path = translation_file_dir / "translation_files.h"

    if common.check_exists_with_existing_artifact_check(path=translation_file_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Running translation generation for Windows")

    # create the file first
    create_command = "cd " + \
        str(translation_file_dir) + " && echo > translation_files.h"
    common.system(create_command)

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    common.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = "bazel run :generate_translations -- " + \
        str(translation_file_path) + " "

    for translation_file in translation_files:
        translated_file_path = translation_file_dir / translation_file

        generation_command = generation_command + " " + \
            str(translated_file_path)

        common.system(generation_command)

    common.check_exists(translation_file_path)


def run_translation_generation_mac(translation_files):
    translation_file_dir = workspace_path / "translations"\

    translation_file_path = translation_file_dir / "translation_files.h"

    if common.check_exists_with_existing_artifact_check(path=translation_file_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Running translation generation for Mac")

    # create the file first
    create_command = "cd " + \
        str(translation_file_dir) + " && echo > translation_files.h"
    common.system(create_command)

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    common.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = "bazel run :generate_translations -- " + \
        str(translation_file_path) + " "

    for translation_file in translation_files:
        translated_file_path = translation_file_dir / translation_file

        generation_command = generation_command + " " + \
            str(translated_file_path)

        common.system(generation_command)

    common.check_exists(translation_file_path)


def translations_generate():
    # first change all the suffixes of the translations files to .qm
    translations_files = convert_translation_files()

    # then run the generation binary with the files as arguments
    run_translation_generation(translations_files)


def translations_generate_win():
    translation_files = convert_translation_files_win()
    run_translation_generation_win(translation_files)


def translations_generate_mac():
    translation_files = convert_translation_files_mac()

    run_translation_generation_mac(translation_files)


def generate_files():
    common.print_something("Generating files")
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate()
    trezor_common()


def generate_files_win():
    common.print_something("Generating files for Windows")
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate_win()
    trezor_common()


def generate_files_mac():
    common.print_something("Generating files for Mac")
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate_mac()
    trezor_common()


def move_own_py_files():
    workspace_path_finder_dest_path = workspace_path / \
        "utils" / "gui" / "workspace_path_finder.py"

    if common.check_exists_with_existing_artifact_check(path=workspace_path_finder_dest_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Moving own py files")

    common.chdir(workspace_path)

    workspace_path_finder_src_path = workspace_path / "workspace_path_finder.py"

    shutil.copyfile(workspace_path_finder_src_path,
                    workspace_path_finder_dest_path)

    common.check_exists(workspace_path_finder_dest_path)

    dest_denarii_client_path = workspace_path / \
        "utils" / "gui" / "denarii_client.py"

    if common.check_exists_with_existing_artifact_check(path=dest_denarii_client_path, delete_single_file=True, fail_on_existence=False):
        return

    src_denarii_client_path = workspace_path / \
        "client" / "Denarii" / "denarii_client.py"

    shutil.copyfile(src_denarii_client_path, dest_denarii_client_path)

    common.check_exists(dest_denarii_client_path)


def move_misc():
    common.print_something("Moving miscellaneous")

    move_own_py_files()


def build_denariid():
    denariid_path = workspace_path / "bazel-bin" / "src" / "denariid"

    if common.check_exists_with_existing_artifact_check(path=denariid_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denariid")

    common.chdir(workspace_path)

    build_command = "bazel build src:denariid"
    common.system(build_command)

    common.check_exists(denariid_path)


def build_denarii_wallet_rpc_server():
    denarii_wallet_rpc_server_path = workspace_path / \
        "bazel-bin" / "src" / "denarii_wallet_rpc_server"

    if common.check_exists_with_existing_artifact_check(path=denarii_wallet_rpc_server_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denarii_wallet_rpc_server")

    common.chdir(workspace_path)

    build_command = "bazel build src:denarii_wallet_rpc_server"
    common.system(build_command)

    common.check_exists(denarii_wallet_rpc_server_path)


def build_binaries():
    common.print_something("Building binaries")

    build_denariid()

    build_denarii_wallet_rpc_server()


def build_denariid_win():

    denariid_win_path = workspace_path / "bazel-bin" / "src" / "denariid.exe"

    if common.check_exists_with_existing_artifact_check(path=denariid_win_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denariid.exe")

    common.chdir(workspace_path)

    build_command = f"bazel {common_bazel_options_windows} build {common_bazel_build_command_options_windows} src:denariid {common_build_options_windows}"
    common.system(build_command)

    common.check_exists(denariid_win_path)


def build_denarii_wallet_rpc_server_win():

    denarii_wallet_rpc_server_win_path = workspace_path / \
        "bazel-bin" / "src" / "denarii_wallet_rpc_server.exe"

    if common.check_exists_with_existing_artifact_check(path=denarii_wallet_rpc_server_win_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denarii_wallet_rpc_server.exe")

    common.chdir(workspace_path)

    build_command = f"bazel {common_bazel_options_windows} build {common_bazel_build_command_options_windows} src:denarii_wallet_rpc_server {common_build_options_windows}"
    common.system(build_command)

    common.check_exists(denarii_wallet_rpc_server_win_path)


def build_binaries_win():
    common.print_something("Building binaries for Windows")

    build_denariid_win()

    build_denarii_wallet_rpc_server_win()


def build_denariid_mac():
    denariid_path = workspace_path / "bazel-bin" / "src" / "denariid"

    if common.check_exists_with_existing_artifact_check(path=denariid_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denariid for Mac")

    common.chdir(workspace_path)

    build_command = "bazel build src:denariid"
    common.system(build_command)

    common.check_exists(denariid_path)


def build_denarii_wallet_rpc_server_mac():

    denarii_wallet_rpc_server_path = workspace_path / \
        "bazel-bin" / "src" / "denarii_wallet_rpc_server"

    if common.check_exists_with_existing_artifact_check(path=denarii_wallet_rpc_server_path, delete_single_file=True, fail_on_existence=False):
        return

    common.print_something("Building denarii_wallet_rpc_server for Mac")

    common.chdir(workspace_path)

    build_command = "bazel build src:denarii_wallet_rpc_server"
    common.system(build_command)

    common.check_exists(denarii_wallet_rpc_server_path)


def build_binaries_mac():
    common.print_something("Building binaries for Mac")

    build_denariid_mac()

    build_denarii_wallet_rpc_server_mac()


def setup_ui():
    common.print_something("Setting up the UI")

    move_misc()

    build_binaries()


def setup_ui_win():
    common.print_something("Setting up the UI for Windows")

    move_misc()

    build_binaries_win()


def setup_ui_mac():
    common.print_something("Setting up the UI for Mac")

    move_misc()

    build_binaries_mac()

def move_external(): 
    # Bazel doesnt find targets in directory named "external" so instead we move it!
    source = workspace_path / "external"
    dest = workspace_path / "other"
    
    if common.check_exists_with_existing_artifact_check(path=dest, delete_tree=True, fail_on_existence=False):
        return
    
    move_command = f"cp -r {source} {dest}"
    common.system(move_command)
    
    common.check_exists(dest)

common.print_something(workspace_path)
if sys.platform == "linux":
    import_dependencies()

    build_dependencies()

    generate_files()
    
    move_external()

    setup_ui()
elif sys.platform == "msys" or sys.platform == "cygwin":
    build_dependencies_win()

    generate_files_win()
    
    move_external()

    setup_ui_win()
elif sys.platform == "darwin":
    import_dependencies_mac()

    build_dependencies_mac()

    generate_files_mac()

    move_external()

    setup_ui_mac()
