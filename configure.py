# Configures some of the install files for Denarii.
# This assumes that Denarii has been cloned into your $HOME repository. Or on Windows your %HOMEDRIVE%%HOMEPATH%
# To see what that is try 'printenv HOME' or 'printenv HOMEDRIVE' and 'printenv HOMEPATH'

import glob
import os
import platform
import re
import requests
import shutil
import subprocess
import sys
import zipfile

import common
import workspace_path_finder

py_pb_files_to_check = ["any_pb2.py", "api_pb2.py", "descriptor_pb2.py", "duration_pb2.py", "empty_pb2.py",
                        "field_mask_pb2.py", "source_context_pb2.py", "struct_pb2.py", "timestamp_pb2.py",
                        "type_pb2.py",
                        "wrappers_pb2.py"]

py_files_to_check = ["descriptor.py", "descriptor_pool.py", "message.py", "reflection.py", "symbol_database.py"]

common_build_options_windows = '--compiler=mingw-gcc --copt="-O3" --copt="-DWIN32_LEAN_AND_MEAN" ' \
                               '--copt="-DMINIUPNP_STATICLIB" --copt="-DZMQ_STATIC" --linkopt="-static" '


class LibraryInfo:

    def __init__(self, libname, foldername=""):
        self.libname = libname
        self.foldername = foldername
        self.folderpath = ""
        self.relevant_paths = []


# note doxygen and graphviz do not work properly
linux_library_info = [LibraryInfo("libnorm-dev", "libnorm"), LibraryInfo("libunbound-dev", "libunbound"),
                      LibraryInfo("libpgm-dev", "openpgm"),
                      LibraryInfo("libsodium-dev", "libsodium"), LibraryInfo("libunwind-dev", "libunwind"),
                      LibraryInfo("liblzma-dev", "liblzma"),
                      LibraryInfo("libreadline-dev", "libreadline"), LibraryInfo("libldns-dev", "ldns"),
                      LibraryInfo("libexpat1-dev", "expat"),
                      LibraryInfo("doxygen", "doxygen"), LibraryInfo("qttools5-dev-tools", "lrelease"),
                      LibraryInfo("graphviz", "graphviz"),
                      LibraryInfo("libhidapi-dev", "libhidapi"), LibraryInfo("libusb-1.0-0-dev", "libusb"),
                      LibraryInfo("libudev-dev", "libudev")]

workspace_path = workspace_path_finder.find_workspace_path()


def download_url(url, save_path, chunk_size=128):
    common.print_something(f"Downloading url {url}")
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

        common.check_exists(path)


def create_folder(libraries):
    common.print_something("Creating folders for libraries")
    external_dir_path = workspace_path / "external"

    for library in libraries:

        foldername = library.foldername

        path = os.path.join(external_dir_path, foldername)

        if not os.path.exists(path):
            os.makedirs(path)

        library.folderpath = path

        common.check_exists(path)


def get_relevant_paths(libraries):
    common.print_something("Gettign relevant paths for libraries")
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

            if ".a" in path or ".so" in path:

                filename = path.split("/")[-1]
                new_path = os.path.join(library.folderpath, filename)

                if os.path.exists(path):
                    common.print_something("Moving: " + path + " to " + library.folderpath)
                    try:
                        if not os.path.exists(new_path):
                            os.mknod(new_path)
                    except:
                        common.print_something("weird this shouldnt happen but is ok")
                    finally:
                        common.print_something(" ALREADY EXISTS " + new_path)
                    shutil.copyfile(path, new_path)

                else:
                    common.print_something(path + " does not exist")


def find_includes(libraries):
    common.print_something("Finding includes for libraries")
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
                        common.print_something("ALREADY EXISTS " + new_path)

                    shutil.copyfile(path, new_path)
                except Exception as e:
                    common.print_something("Could not copy file " + path)
                    common.print_something(e)


def import_dependencies():
    common.print_something("Importing dependencies")
    create_folder(linux_library_info)
    create_build_file(linux_library_info)
    get_relevant_paths(linux_library_info)
    find_includes(linux_library_info)
    find_src_files(linux_library_info)


def miniupnp(external_dir_path):
    common.print_something("Getting miniupnp")
    raw_path = str(external_dir_path)

    # remove the empty directory
    remove_command = "rm -rf " + raw_path + "/miniupnp"
    common.system(remove_command)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone https://github.com/miniupnp/miniupnp.git"
    common.system(clone_command)

    # we only need to build one of the subdirectories
    miniupnp_path = raw_path + "/miniupnp/miniupnpc"

    common.chdir(miniupnp_path)

    command = "sudo make install"
    common.system(command)

    common.check_exists(miniupnp_path)


def randomx(external_dir_path):
    common.print_something("Getting randomx")
    raw_path = str(external_dir_path)

    randomx_path = raw_path + "/randomx"

    common.chdir(randomx_path)

    command = "mkdir build && cd build && cmake -DARCH=native .. && make"
    common.system(command)

    common.check_exists(randomx_path)


def supercop(external_dir_path):
    common.print_something("Getting supercop")
    raw_path = str(external_dir_path)

    common.chdir(raw_path)

    supercop_path = raw_path + "/supercop"

    remove_command = "rm -rf " + supercop_path
    common.system(remove_command)

    clone_command = "git clone --recursive https://github.com/andrewkatson/supercop.git && cd supercop && git submodule init && git submodule update"
    common.system(clone_command)

    common.chdir(supercop_path)

    # need to create the first crypto library 
    first_create_command = "cmake . && make && sudo make install"
    common.system(first_create_command)

    first_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto64.a"
    common.system(first_move_command)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && sudo make install"
    common.system(second_create_command)

    second_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto.a"
    common.system(second_move_command)

    common.check_exists(supercop_path)


def supercop_win(external_dir_path):
    common.print_something("Getting supercop for Windows")
    raw_path = str(external_dir_path)

    common.chdir(raw_path)

    supercop_path = raw_path + "/supercop"

    remove_command = "rm -rf " + supercop_path
    common.system(remove_command)

    clone_command = "git clone --recursive https://github.com/andrewkatson/supercop.git && git submodule init && git submodule update"
    common.system(clone_command)

    common.chdir(supercop_path)

    # need to create the first crypto library
    first_create_command = "cmake . && make && make install"
    common.system(first_create_command)

    first_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto64.a"
    common.system(first_move_command)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && make install"
    common.system(second_create_command)

    second_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto.a"
    common.system(second_move_command)

    common.check_exists(supercop_path)


def unbound(external_dir_path):
    common.print_something("Getting unbound")
    raw_path = str(external_dir_path)

    unbound_path = raw_path + "/unbound"

    common.chdir(unbound_path)

    command = "./configure && make && sudo make install"
    common.system(command)

    move_command = "mv /usr/local/lib/libunbound.so " + unbound_path
    common.system(move_command)

    common.check_exists(unbound_path)


def openssl(external_dir_path):
    common.print_something("Getting openssl")
    raw_path = str(external_dir_path)

    common.chdir(raw_path)

    openssl_zip_path = raw_path + "/openssl.zip"
    download_url("https://www.openssl.org/source/openssl-1.1.1i.tar.gz", openssl_zip_path)

    unzip_command = "tar -xvzf " + openssl_zip_path + " -C " + raw_path
    common.system(unzip_command)

    openssl_path = raw_path + "/openssl"

    openssl_wrong_name_path = raw_path + "/openssl-1.1.1i"
    rename_command = "mv " + openssl_wrong_name_path + " " + openssl_path
    common.system(rename_command)

    common.chdir(openssl_path)

    command = "./config && make && make test"
    common.system(command)

    common.check_exists(openssl_path)


def libzmq(external_dir_path):
    common.print_something("Getting libzmq")
    raw_path = str(external_dir_path)

    clone_command = "git clone https://github.com/zeromq/libzmq.git"
    common.system(clone_command)

    libzmq_path = raw_path + "/libzmq"

    common.chdir(libzmq_path)

    command = "./autogen.sh && ./configure --with-libsodium && make && sudo make install"
    common.system(command)

    move_command = "mv /usr/local/lib/libzmq.a " + libzmq_path
    common.system(move_command)

    common.check_exists(libzmq_path)


def zlib(external_dir_path):
    common.print_something("Getting zlib")
    raw_path = str(external_dir_path)

    zlib_path = raw_path + "/zlib"

    common.chdir(zlib_path)

    command = "./configure && make test && sudo make install"
    common.system(command)

    common.check_exists(zlib_path)


def liblmdb(external_dir_path):
    common.print_something("Getting liblmdb")
    liblmdb_path = external_dir_path / "db_drivers/liblmdb"

    common.chdir(liblmdb_path)
    command = "make"
    common.system(command)

    common.check_exists(liblmdb_path)


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


def build_dependencies_win():
    common.print_something("Building dependencies for Windows")
    external_dir_path = workspace_path / "external"

    common.chdir(external_dir_path)
    supercop_win(external_dir_path)
    common.chdir(external_dir_path)


def trezor_common():
    text = 'load(\"@rules_proto//proto:defs.bzl\", \"proto_library\")  \n\
load(\"@rules_cc//cc:defs.bzl\", \"cc_proto_library\")     \n\
package(default_visibility = [\"//visibility:public\"])  \n\
cc_proto_library(                                      \n\
 name = \"messages_cc_proto\",                        \n\
 deps = [\":messages_proto\"],                        \n\
)                                                      \n\
proto_library(                                         \n\
 name = \"messages_proto\",                           \n\
 srcs = [\"messages.proto\"],                         \n\
 deps = [                                           \n\
     \"@com_google_protobuf//:descriptor_proto\",     \n\
 ],                                                 \n\
)                                                      \n\
cc_proto_library(                                      \n\
 name = \"messages_common_cc_proto\",                 \n\
 deps = [\":messages_common_proto\"],                 \n\
)                                                      \n\
proto_library(                                         \n\
 name = \"messages_common_proto\",                    \n\
 srcs = [\"messages-common.proto\"],                  \n\
 deps = [                                           \n\
 ],                                                 \n\
)                                                      \n\
cc_proto_library(                                      \n\
 name = \"messages_management_cc_proto\",             \n\
 deps = [\":messages_management_proto\"],             \n\
)                                                      \n\
proto_library(                                         \n\
 name = \"messages_management_proto\",                \n\
 srcs = [\"messages-management.proto\"],              \n\
 deps = [                                           \n\
 ],                                                 \n\
)                                                      \n\
cc_proto_library(                                      \n\
 name = \"messages_monero_cc_proto\",                 \n\
 deps = [\":messages_monero_proto\"],                 \n\
)                                                      \n\
proto_library(                                         \n\
 name = \"messages_monero_proto\",                    \n\
 srcs = [\"messages-monero.proto\"],                  \n\
 deps = [                                           \n\
 ],                                                 \n\
)'
    common.print_something("Setting up trezor common")

    path_to_dir = str(workspace_path) + "/external/trezor-common/protob"
    common.chdir(path_to_dir)

    common.system(f"echo \'{text}\' > BUILD")

    path_to_workspace_dir = str(workspace_path) + "/external/trezor-common"
    common.chdir(path_to_workspace_dir)

    workspace_text = f'workspace(name = \"trezor_common\") \n\
load(\"@bazel_tools//tools/build_defs/repo:http.bzl\", \"http_archive\")   \n\
# rules_proto defines abstract rules for building Protocol Buffers. \n\
http_archive( \n\
    name = \"rules_proto\", \n\
    sha256 = \"602e7161d9195e50246177e7c55b2f39950a9cf7366f74ed5f22fd45750cd208\", \n\
    strip_prefix = \"rules_proto-97d8af4dc474595af3900dd85cb3a29ad28cc313\", \n\
    urls = [ \n\
        \"https://mirror.bazel.build/github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz\", \n\
        \"https://github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz\", \n\
    ], \n\
) \n\
load(\"@rules_proto//proto:repositories.bzl\", \"rules_proto_dependencies\", \"rules_proto_toolchains\") \n\
rules_proto_dependencies() \n\
rules_proto_toolchains()'

    common.system(f"echo \'{workspace_text}\' > WORKSPACE")

    common.check_exists(path_to_workspace_dir)


def blocks_generate():
    common.print_something("Generating blocks files")
    input_files = ["checkpoints.dat", "stagenet_blocks.dat", "testnet_blocks.dat"]
    output_files = ["generated_checkpoints.c", "generated_stagenet_blocks.c", "generated_testnet_blocks.c"]
    base_names = ["checkpoints", "stagenet_blocks", "testnet_blocks"]

    for i in range(len(input_files)):
        input_file = input_files[i]
        output_file = output_files[i]
        base_name = base_names[i]

        path_to_blocks = str(workspace_path) + "/src/blocks"
        command = "cd " + path_to_blocks + " && echo '#include\t<stddef.h>\n#ifndef _WIN32' > " + output_file \
                  + " && echo 'const\tunsigned\tchar\t" + base_name + "[]={' >> " + output_file + " && od -v -An -tx1 " \
                  + input_file + " | sed -e 's/[0-9a-fA-F]\\{1,\\}/0x&,/g' -e '$s/.$//' >> " + output_file + " && echo '};' >> " + output_file \
                  + " && echo 'const\tsize_t\t" + base_name + "_len\t=\tsizeof(" + base_name + ");\n#endif' >> " + output_file

        common.system(command)

    for output in output_files:
        path_to_output = workspace_path / "src" / "blocks" / output
        common.check_exists(path_to_output)


def crypto_wallet_generate():
    common.print_something("Generating crypto wallet directory")
    crypto_wallet_path = str(workspace_path) + "/src/crypto/wallet"
    ops_file = "ops.h"
    build_file = "BUILD"

    supercop_path = str(workspace_path) + "/external/supercop"
    copy_file_path = supercop_path + "/include/monero/crypto.h"

    # If we are on Linux and have 64 bit processor we can use monero's default crypto libraries
    if re.match(".*nix.*|.*ux.*", platform.common.system()) and re.match(".*amd64.*|.*AMD64.*|.*x86_64.*",
                                                                         platform.processor()):

        # copy the contents of the crypto file over to ops
        with open(copy_file_path, "r") as copy:
            # generate the file
            command = "cd " + crypto_wallet_path + " && echo > " + ops_file
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
                    copy_line_command = "cd " + crypto_wallet_path + " && echo '" + modified_line + "' >> " + ops_file
                    common.system(copy_line_command)

                elif seen_license_info and "#include \"monero/crypto/amd64-51-30k.h\"" in line:
                    # we have to output a different line than the include in this line because
                    # bazel will not be viewing that dependency in the same way that cmake does
                    modified_line = "#include \"include/monero/crypto/amd64-51-30k.h\""
                    copy_line_command = "cd " + crypto_wallet_path + " && echo '" + modified_line + "' >> " + ops_file
                    common.system(copy_line_command)

                elif seen_license_info:
                    copy_line_command = "cd " + crypto_wallet_path + " && echo '" + line + "' >> " + ops_file
                    common.system(copy_line_command)
    else:
        # Otherwise create an empty file.
        command = "cd " + crypto_wallet_path + " && touch " + ops_file + " && echo \"#pragma once\" >> " + ops_file
        common.system(command)


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
            common.print_something('Unable to get version number from git tags')
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

    src_directory = str(workspace_path) + "/src/"

    input_file_path = os.path.join(src_directory, input_file)
    with open(input_file_path, "r") as copy:

        # create the file
        create_file_command = "cd " + src_directory + " && echo > " + output_file
        common.system(create_file_command)

        for line in copy:
            line_to_write = line
            if version_tag_str in line:
                line_to_write = line.replace(version_tag_str, version_tag)

            if version_release_str in line:
                line_to_write = line.replace(version_release_str, str(is_release).lower())

            write_line_command = "cd " + src_directory + " && echo '" + line_to_write + "' >> " + output_file
            common.system(write_line_command)


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

    tests_directory = str(workspace_path) + "/tests/"

    input_file_path = os.path.join(tests_directory, input_file)

    with open(input_file_path, "r") as copy:

        for line in copy:
            line_to_write = line

            if benchmark_str in line:
                line_to_write = line.replace(benchmark_str, replacement)

            write_line_command = "cd " + tests_directory + " && echo '" + line_to_write + "' >> " + output_file
            common.system(write_line_command)


def benchmark_generate():
    replacement = ""

    # If we are on Linux and have 64 bit processor we can use monero's default crypto libraries
    if re.match(".*nix.*|.*ux.*", platform.common.system()) and re.match(".*amd64.*|.*AMD64.*|.*x86_64.*",
                                                                         platform.processor()):
        replacement = "(cn)(amd64_64_24k)(amd64_51_30k)"
    else:
        replacement = "(cn)"

    generate_benchmark_file_with_replacement(replacement)


def convert_translation_files():
    common.print_something("Conveting translation files")
    translation_file_dir = str(workspace_path) + "/translations"

    common.chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        file = files[i]
        converted_file = converted_files[i]

        conversion_command = "lrelease " + file + " -qm " + converted_file
        common.system(conversion_command)

    return converted_files


def convert_translation_files_win():
    common.print_something("Converting translation files for Windows")
    translation_file_dir = str(workspace_path) + "/translations"

    common.chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        file = files[i]
        converted_file = converted_files[i]

        conversion_command = "/mingw64/bin/lrelease " + file + " -qm " + converted_file
        common.system(conversion_command)

    return converted_files


def run_translation_generation(translation_files):
    common.print_something("Running translation generation")
    translation_file_dir = str(workspace_path) + "/translations"
    # create the file first
    create_command = "cd " + translation_file_dir + " && echo > translation_files.h"
    common.system(create_command)

    translation_file_path = translation_file_dir + "/translation_files.h"

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    common.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = str(
        workspace_path) + "/bazel-bin/translations/generate_translations " + translation_file_path + " "

    for translation_file in translation_files:
        generation_command = generation_command + " " + translation_file_dir + "/" + translation_file

    common.system(generation_command)


def run_translation_generation_win(translation_files):
    common.print_something("Running translation generation for Windows")
    translation_file_dir = str(workspace_path) + "/translations"

    # create the file first
    create_command = "cd " + translation_file_dir + " && echo > translation_files.h"
    common.system(create_command)

    translation_file_path = translation_file_dir + "/translation_files.h"

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    common.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = "bazel run :generate_translations -- " + translation_file_path + " "

    for translation_file in translation_files:
        generation_command = generation_command + " " + translation_file_dir + "/" + translation_file

    common.system(generation_command)


def translations_generate():
    # first change all the suffixes of the translations files to .qm
    translations_files = convert_translation_files()

    # then run the generation binary with the files as arguments
    run_translation_generation(translations_files)


def translations_generate_win():
    translation_files = convert_translation_files_win()
    run_translation_generation_win(translation_files)


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


def download_keiros_public():
    common.print_something("Downloading KeirosPublic")

    path = workspace_path / "external"
    common.chdir(path)

    clone_command = "git clone https://github.com/andrewkatson/KeirosPublic.git"
    common.system(clone_command)

    keiros_public_path = path / "KeirosPublic"
    common.check_exists(keiros_public_path)


def download_protobuf():
    common.print_something("Downloading Google Protobuf")

    url = "https://github.com/protocolbuffers/protobuf/archive/refs/tags/v21.9.zip"
    save_path = workspace_path / "external" / "protobuf.zip"
    download_url(url, save_path)

    final_path = workspace_path / "external" / "protobuf"
    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(final_path)


def download_dependencies_for_ui():
    common.print_something("Downloading dependencies for ui")
    download_keiros_public()

    download_protobuf()


def build_keiros_public_protos():
    common.print_something("Building KeirosPublic protos")

    keiros_public_path = workspace_path / "external" / "KeirosPublic"
    common.chdir(keiros_public_path)

    build_command = "bazel build Proto:wallet_py_proto"
    common.system(build_command)

    wallet_py_proto_path = workspace_path / "bazel-bin" / "Proto" / "wallet_pb2.py"
    common.check_exists(wallet_py_proto_path)

    other_build_command = "bazel build Security:identifier_py_proto"
    common.system(other_build_command)

    identifier_py_proto_path = workspace_path / "bazel-bin" / "Security" / "identifier_pb2.py"
    common.check_exists(identifier_py_proto_path)


def build_google_protobuf_protos():
    common.print_something("Building Google Protobuf protos")

    google_protobuf_path = workspace_path / "external" / "protobuf"
    common.chdir(google_protobuf_path)

    build_command = "bazel build :well_known_types_py_pb2"
    common.system(build_command)

    base_path = google_protobuf_path / "bazel-bin" / "python" / "google" / "protobuf"
    for file in py_pb_files_to_check:
        path = base_path / file
        common.check_exists(path)


def build_own_protos():
    common.print_something("Building own protos")

    common.chdir(workspace_path)

    build_command = "bazel build utils/gui/Proto:all"
    common.system(build_command)

    path = workspace_path / "bazel-bin" / "utils" / "gui" / "Proto" / "gui_user_pb2.py"
    common.check_exists(path)


def build_protos():
    common.print_something("Building protos")

    build_keiros_public_protos()

    build_google_protobuf_protos()

    build_own_protos()


def move_keiros_public_protos():
    common.print_something("Moving KeirosPublic protos")

    common.chdir(workspace_path)

    keiros_public_path = workspace_path / "external" / "KeirosPublic"

    src_wallet_py_path = keiros_public_path / "bazel-bin" / "Proto" / "wallet_pb2.py"
    dest_wallet_py_path = workspace_path / "utils" / "gui" / "Proto" / "wallet_pb2.py"

    shutil.copyfile(src_wallet_py_path, dest_wallet_py_path)

    common.check_exists(dest_wallet_py_path)

    src_identifier_py_path = keiros_public_path / "bazel-bin" / "Security" / "identifier_pb2.py"
    dest_identifier_py_path = workspace_path / "utils" / "gui" / "Security" / "identifier_pb2.py"

    shutil.copyfile(src_identifier_py_path, dest_identifier_py_path)

    common.check_exists(dest_identifier_py_path)


def move_google_protobuf_protos():
    common.print_something("Moving Google Protobuf protos")

    common.chdir(workspace_path)

    google_protobuf_path = workspace_path / "external" / "protobuf"

    common_src_path = google_protobuf_path / "bazel-bin" / "python" / "google" / "protobuf"
    common_dest_path = workspace_path / "utils" / "gui" / "google" / "protobuf"

    for file in py_pb_files_to_check:
        src_path = common_src_path / file
        dest_path = common_dest_path / file
        shutil.copyfile(src_path, dest_path)

        common.check_exists(dest_path)


def move_own_protos():
    common.print_something("Moving own protos")

    common.chdir(workspace_path)

    gui_user_path = workspace_path / "bazel-bin" / "utils" / "gui" / "Proto" / "gui_user_pb2.py"
    gui_user_dest_path = workspace_path / "utils" / "gui" / "Proto" / "gui_user_pb2.py"

    shutil.copyfile(gui_user_path, gui_user_dest_path)

    common.check_exists(gui_user_dest_path)


def move_protos():
    common.print_something("Moving protos")

    move_keiros_public_protos()

    move_google_protobuf_protos()

    move_own_protos()


def move_keiros_public_py_files():
    common.print_something("Moving KeirosPublic py files")

    common.chdir(workspace_path)

    src_denarii_client_path = workspace_path / "external" / "KeirsoPublic" / "Client" / "Denarii" / "denarii_client.py"
    dest_denarii_client_path = workspace_path / "utils" / "gui" / "denarii_client.py"

    shutil.copyfile(src_denarii_client_path, dest_denarii_client_path)

    common.check_exists(dest_denarii_client_path)


def move_google_protobuf_py_files():
    common.print_something("Moving google protobuf py files")

    common.chdir(workspace_path)

    common_src_path = workspace_path / "external" / "protobuf" / "python" / "google" / "protobuf"
    common_dest_path = workspace_path / "utils" / "gui" / "google" / "protobuf"

    for file in py_files_to_check:
        src_path = common_src_path / file
        dest_path = common_dest_path / file
        shutil.copyfile(src_path, dest_path)

        common.check_exists(dest_path)


def move_own_py_files():
    common.print_something("Moving own py files")

    common.chdir(workspace_path)

    workspace_path_finder_src_path = workspace_path / "workspace_path_finder.py"
    workspace_path_finder_dest_path = workspace_path / "utils" / "gui" / "workspace_path_finder.py"

    shutil.copyfile(workspace_path_finder_src_path, workspace_path_finder_dest_path)

    common.check_exists(workspace_path_finder_dest_path)


def move_misc():
    common.print_something("Moving miscellaneous")

    move_keiros_public_py_files()

    move_google_protobuf_py_files()

    move_own_py_files()


def build_denariid():
    common.print_something("Building denariid")

    common.chdir(workspace_path)

    build_command = "bazel_build src:denariid"
    common.system(build_command)

    denariid_path = workspace_path / "bazel-bin" / "src" / "denariid"
    common.check_exists(denariid_path)


def build_denarii_wallet_rpc_server():
    common.print_something("Building denarii_wallet_rpc_server")

    common.chdir(workspace_path)

    build_command = "bazel build src:denarii_wallet_rpc_server"
    common.system(build_command)

    denarii_wallet_rpc_server_path = workspace_path / "bazel-bin" / "src" / "denarii_wallet_rpc_server"
    common.check_exists(denarii_wallet_rpc_server_path)


def build_binaries():
    common.print_something("Building binaries")

    build_denariid()

    build_denarii_wallet_rpc_server()


def build_denariid_win():
    common.print_something("Building denariid.exe")

    common.chdir(workspace_path)

    build_command = f"bazel build src:denariid {common_build_options_windows}"
    common.system(build_command)

    denariid_win_path = workspace_path / "bazel-bin" / "src" / "denariid.exe"
    common.check_exists(denariid_win_path)


def build_denarii_wallet_rpc_server_win():
    common.print_something("Building denarii_wallet_rpc_server.exe")

    common.chdir(workspace_path)

    build_command = f"bazel build src:denarii_wallet_rpc_server {common_build_options_windows}"
    common.system(build_command)

    denarii_wallet_rpc_server_win_path = workspace_path / "bazel-bin" / "src" / "denarii_wallet_rpc_server.exe"
    common.check_exists(denarii_wallet_rpc_server_win_path)


def build_binaries_win():
    common.print_something("Building binaries for Windows")

    build_denariid_win()

    build_denarii_wallet_rpc_server_win()


def move_denariid():
    common.print_something("Moving denariid")

    common.chdir(workspace_path)

    src_path = workspace_path / "bazel-bin" / "src" / "denariid"
    dest_path = workspace_path / "utils" / "gui" / "denariid"
    shutil.copyfile(src_path, dest_path)

    common.check_exists(dest_path)


def move_denarii_wallet_rpc_server():
    common.print_something("Moving denarii_wallet_rpc_server")

    common.chdir(workspace_path)

    src_path = workspace_path / "bazel-bin" / "src" / "denarii_wallet_rpc_server"
    dest_path = workspace_path / "utils" / "gui" / "denarii_wallet_rpc_server"
    shutil.copyfile(src_path, dest_path)

    common.check_exists(dest_path)


def move_binaries():
    common.print_something("Moving binaries")

    move_denariid()

    move_denarii_wallet_rpc_server()


def move_denariid_win():
    common.print_something("Moving denariid.exe")

    common.chdir(workspace_path)

    src_path = workspace_path / "bazel-bin" / "src" / "denariid.exe"
    dest_path = workspace_path / "utils" / "gui" / "denariid.exe"
    shutil.copyfile(src_path, dest_path)

    common.check_exists(dest_path)


def move_denarii_wallet_rpc_server_win():
    common.print_something("Moving denarii_wallet_rpc_server.exe")

    common.chdir(workspace_path)

    src_path = workspace_path / "bazel-bin" / "src" / "denarii_wallet_rpc_server.exe"
    dest_path = workspace_path / "utils" / "gui" / "denarii_wallet_rpc_server.exe"
    shutil.copyfile(src_path, dest_path)

    common.check_exists(dest_path)


def move_binaries_win():
    common.print_something("Moving binaries for Windows")

    move_denariid_win()

    move_denarii_wallet_rpc_server_win()


def setup_ui():
    common.print_something("Setting up the UI")
    download_dependencies_for_ui()

    build_protos()

    move_protos()

    move_misc()

    build_binaries()

    move_binaries()


def setup_ui_win():
    common.print_something("Setting up the UI for Windows")
    download_dependencies_for_ui()

    build_protos()

    move_protos()

    move_misc()

    build_binaries_win()

    move_binaries_win()


common.print_something(workspace_path)
if sys.platform == "linux":
    import_dependencies()

    build_dependencies()

    generate_files()

    setup_ui()
elif sys.platform == "msys":

    build_dependencies_win()

    generate_files_win()

    setup_ui_win()
