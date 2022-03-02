# Configures some of the install files for denarii.
# This assumes that denarii has been cloned into your $HOME repository.
# To see what that is try 'printenv HOME'

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

parser = argparse.ArgumentParser(description="Process command line flags")
parser.add_argument('--workspace_path', type=str, help='The path to the relevant WORKSPACE file', default='')

args = parser.parse_args()

workspace_path = pathlib.Path()


def chdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(path)


def find_workspace_path():
    global workspace_path

    if args.workspace_path == '':
        # Need to explicitly set this or pass it in as a variable.
        linux_workspace_path = pathlib.Path("/home/andrew/denarii")
        windows_workspace_path = pathlib.Path("C:/Users/katso/Documents/Github/denarii")

        # A workspace path that works if not sudo on EC2
        try:
            possible_workspace_path = pathlib.Path(os.environ["HOME"] + "/denarii")
            if os.path.exists(possible_workspace_path):
                workspace_path = possible_workspace_path
        except Exception as e:
            print(e)
            print("The HOME variable does not point to the directory")

        # A workspace path that works in sudo on EC2
        try:
            possible_workspace_path = pathlib.Path("/home/" + os.environ["SUDO_USER"] + "/denarii")

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
        workspace_path = Path(args.workspace_path)


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def create_build_file(libraries):
    external_dir_path = workspace_path / "external"

    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(external_dir_path, build_file_name)

        if not os.path.exists(path):
            os.mknod(path)


def create_folder(libraries):
    external_dir_path = workspace_path / "external"

    for library in libraries:

        foldername = library.foldername

        path = os.path.join(external_dir_path, foldername)

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


def import_dependencies():
    create_folder(linux_library_info)
    create_build_file(linux_library_info)
    get_relevant_paths(linux_library_info)
    find_includes(linux_library_info)
    find_src_files(linux_library_info)


def miniupnp(external_dir_path):
    raw_path = str(external_dir_path.stem)

    # remove the empty directory
    remove_command = "rm -rf " + raw_path + "/miniupnp"
    os.system(remove_command)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone https://github.com/miniupnp/miniupnp.git"
    os.system(clone_command)

    # we only need to build one of the subdirectories
    miniupnp_path = raw_path + "/miniupnp/miniupnpc"

    chdir(miniupnp_path)

    command = "sudo make install"
    os.system(command)


def miniupnp_win(external_dir_path):
    raw_path = str(external_dir_path)

    # remove the empty directory
    remove_command = "rm -rf " + raw_path + "/external/miniupnp"
    os.system(remove_command)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone https://github.com/miniupnp/miniupnp.git"
    os.system(clone_command)

    # we only need to build one of the subdirectories
    miniupnp_path = raw_path + "/external/miniupnp/miniupnpc"

    chdir(miniupnp_path)

    command = "cmake . && make && ./mingw32make.bat"
    os.system(command)


def randomx(external_dir_path):
    raw_path = str(external_dir_path)

    randomx_path = raw_path + "/randomx"

    chdir(randomx_path)

    command = "mkdir build && cd build && cmake -DARCH=native .. && make"
    os.system(command)


def supercop(external_dir_path):
    raw_path = str(external_dir_path)

    chdir(raw_path)

    supercop_path = raw_path + "/supercop"

    remove_command = "rm -rf " + supercop_path
    os.system(remove_command)

    clone_command = "git clone https://github.com/andrewkatson/supercop.git"
    os.system(clone_command)

    chdir(supercop_path)

    # need to create the first crypto library 
    first_create_command = "cmake . && make && sudo make install"
    os.system(first_create_command)

    first_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto64.a"
    os.system(first_move_command)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && sudo make install"
    os.system(second_create_command)

    second_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto.a"
    os.system(second_move_command)


def supercop_win(external_dir_path):
    raw_path = str(external_dir_path)

    chdir(raw_path)

    supercop_path = raw_path + "/supercop"

    remove_command = "rm -rf " + supercop_path
    os.system(remove_command)

    clone_command = "git clone https://github.com/andrewkatson/supercop.git"
    os.system(clone_command)

    chdir(supercop_path)

    # need to create the first crypto library
    first_create_command = "cmake . && make && make install"
    os.system(first_create_command)

    first_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto64.a"
    os.system(first_move_command)

    # then create its sibling
    second_create_command = "cmake . -DMONERO_CRYPTO_LIBRARY=amd64-51-30k && make && make install"
    os.system(second_create_command)

    second_move_command = "mv /usr/local/lib/libmonero-crypto.a " + supercop_path + "/libmonero-crypto.a"
    os.system(second_move_command)


def unbound(external_dir_path):
    raw_path = str(external_dir_path)

    unbound_path = raw_path + "/unbound"

    chdir(unbound_path)

    command = "./configure && make && sudo make install"
    os.system(command)

    move_command = "mv /usr/local/lib/libunbound.so " + unbound_path
    os.system(move_command)


def openssl(external_dir_path):
    raw_path = str(external_dir_path)

    chdir(raw_path)

    openssl_zip_path = raw_path + "/openssl.zip"
    download_url("https://www.openssl.org/source/openssl-1.1.1i.tar.gz", openssl_zip_path)

    unzip_command = "tar -xvzf " + openssl_zip_path + " -C " + raw_path
    os.system(unzip_command)

    openssl_path = raw_path + "/openssl"

    openssl_wrong_name_path = raw_path + "/openssl-1.1.1i"
    rename_command = "mv " + openssl_wrong_name_path + " " + openssl_path
    os.system(rename_command)

    chdir(openssl_path)

    command = "./config && make && make test"
    os.system(command)


def libzmq(external_dir_path):
    raw_path = str(external_dir_path)

    clone_command = "git clone https://github.com/zeromq/libzmq.git"
    os.system(clone_command)

    libzmq_path = raw_path + "/libzmq"

    chdir(libzmq_path)

    command = "./autogen.sh && ./configure --with-libsodium && make && sudo make install"
    os.system(command)

    move_command = "mv /usr/local/lib/libzmq.a " + libzmq_path
    os.system(move_command)


def zlib(external_dir_path):
    raw_path = str(external_dir_path)

    zlib_path = raw_path + "/zlib"

    chdir(zlib_path)

    command = "./configure && make test && sudo make install"
    os.system(command)


def liblmdb(external_dir_path):
    liblmdb_path = external_dir_path / "db_drivers/liblmdb"

    chdir(liblmdb_path)
    command = "make"
    os.system(command)


def build_dependencies():
    external_dir_path = workspace_path / "external"
    chdir(external_dir_path)

    miniupnp(external_dir_path)

    chdir(external_dir_path)
    randomx(external_dir_path)

    chdir(external_dir_path)
    supercop(external_dir_path)

    chdir(external_dir_path)
    unbound(external_dir_path)

    chdir(external_dir_path)
    openssl(external_dir_path)

    chdir(external_dir_path)
    libzmq(external_dir_path)

    chdir(external_dir_path)
    zlib(external_dir_path)

    chdir(external_dir_path)

    liblmdb(external_dir_path)
    chdir(external_dir_path)


def build_dependencies_win():
    external_dir_path = workspace_path / "external"

    chdir(external_dir_path)
    supercop_win(external_dir_path)
    chdir(external_dir_path)


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

    path_to_dir = str(workspace_path) + "/external/trezor-common/protob"
    chdir(path_to_dir)

    os.system(f"echo \'{text}\' > BUILD")

    path_to_workspace_dir = str(workspace_path) + "/external/trezor-common"
    chdir(path_to_workspace_dir)

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

    os.system(f"echo \'{workspace_text}\' > WORKSPACE")


def blocks_generate():
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

        os.system(command)


def crypto_wallet_generate():
    crypto_wallet_path = str(workspace_path) + "/src/crypto/wallet"
    ops_file = "ops.h"
    build_file = "BUILD"

    supercop_path = str(workspace_path) + "/external/supercop"
    copy_file_path = supercop_path + "/include/monero/crypto.h"

    # If we are on Linux and have 64 bit processor we can use monero's default crypto libraries
    if re.match(".*nix.*|.*ux.*", platform.system()) and re.match(".*amd64.*|.*AMD64.*|.*x86_64.*",
                                                                  platform.processor()):

        # copy the contents of the crypto file over to ops
        with open(copy_file_path, "r") as copy:
            # generate the file
            command = "cd " + crypto_wallet_path + " && echo > " + ops_file
            os.system(command)

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
                    os.system(copy_line_command)

                elif seen_license_info:
                    copy_line_command = "cd " + crypto_wallet_path + " && echo '" + line + "' >> " + ops_file
                    os.system(copy_line_command)


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
    d = str(workspace_path)

    if os.path.isdir(os.path.join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git rev-parse --short=9 HEAD'.split()
        try:
            version = subprocess.check_output(cmd).decode().strip()
        except subprocess.CalledProcessError:
            print('Unable to get version number from git tags')
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
            print('Unable to get git index status')
            exit(1)

        if dirty != '':
            version += '.dev1'

    else:
        # Extract the version from the PKG-INFO file.
        with open(os.path.join(d, 'PKG-INFO')) as f:
            version = version_re.search(f.read()).group(1)

    return version


def generate_version_file_with_replacement(version_tag, is_release):
    version_tag_str = "@VERSIONTAG@"
    version_release_str = "@VERSION_IS_RELEASE@"

    input_file = "version.cpp.in"
    output_file = "version.cpp"

    src_directory = str(workspace_path) + "/src/"

    input_file_path = os.path.join(src_directory, input_file)
    with open(input_file_path, "r") as copy:

        # create the file
        create_file_command = "cd " + src_directory + " && echo > " + output_file
        os.system(create_file_command)

        for line in copy:
            line_to_write = line
            if version_tag_str in line:
                line_to_write = line.replace(version_tag_str, version_tag)

            if version_release_str in line:
                line_to_write = line.replace(version_release_str, str(is_release).lower())

            write_line_command = "cd " + src_directory + " && echo '" + line_to_write + "' >> " + output_file
            os.system(write_line_command)


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
            os.system(write_line_command)


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
    translation_file_dir = str(workspace_path) + "/translations"

    chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        file = files[i]
        converted_file = converted_files[i]

        conversion_command = "lrelease " + file + " -qm " + converted_file
        os.system(conversion_command)

    return converted_files


def convert_translation_files_win():
    translation_file_dir = str(workspace_path) + "/translations"

    chdir(translation_file_dir)

    files = []
    converted_files = []

    for file in glob.glob("*.ts"):
        files.append(file)
        converted_files.append(file.replace(".ts", ".qm"))

    for i in range(len(files)):
        file = files[i]
        converted_file = converted_files[i]

        conversion_command = "/mingw64/bin/lrelease " + file + " -qm " + converted_file
        os.system(conversion_command)

    return converted_files


def run_translation_generation(translation_files):
    translation_file_dir = str(workspace_path) + "/translations"
    # create the file first
    create_command = "cd " + translation_file_dir + " && echo > translation_files.h"
    os.system(create_command)

    translation_file_path = translation_file_dir + "/translation_files.h"

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    os.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = str(
        workspace_path) + "/bazel-bin/translations/generate_translations " + translation_file_path + " "

    for translation_file in translation_files:
        generation_command = generation_command + " " + translation_file_dir + "/" + translation_file

    os.system(generation_command)


def run_translation_generation_win(translation_files):
    translation_file_dir = str(workspace_path) + "/translations"

    # create the file first
    create_command = "cd " + translation_file_dir + " && echo > translation_files.h"
    os.system(create_command)

    translation_file_path = translation_file_dir + "/translation_files.h"

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    os.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = "bazel run :generate_translations -- " + translation_file_path + " "

    for translation_file in translation_files:
        generation_command = generation_command + " " + translation_file_dir + "/" + translation_file

    os.system(generation_command)


def translations_generate():
    # first change all the suffixes of the translations files to .qm
    translations_files = convert_translation_files()

    # then run the generation binary with the files as arguments
    run_translation_generation(translations_files)


def translations_generate_win():
    translation_files = convert_translation_files_win()
    run_translation_generation_win(translation_files)


def generate_files():
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate()
    trezor_common()


def generate_files_win():
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate_win()
    trezor_common()


find_workspace_path()
print(workspace_path)
if sys.platform == "linux":
    print("Importing dependencies \n\n\n\n\n")
    import_dependencies()

    print("Building dependencies \n\n\n\n\n")
    build_dependencies()

    print ("Generating files \n\n\n\n\n")
    generate_files()
elif sys.platform == "msys":

    print("Building dependencies Windows \n\n\n\n\n")
    build_dependencies_win()

    print("Generating files Windows \n\n\n\n\n")
    generate_files_win()

    print("Miniupnp Windows \n\n\n\n\n")
    # We have to do this last because it will just hang.
    external_dir_path = workspace_path / "external"
    chdir(external_dir_path)
    miniupnp_win(workspace_path)
