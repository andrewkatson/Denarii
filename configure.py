# Configures some of the install files for denarii.
# This assumes that denarii has been cloned into your $HOME repository.
# To see what that is try 'printenv HOME'

import glob
import os
import pathlib
import platform
import psutil
import re
import requests
import shutil
import subprocess
import zipfile


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

# NEED TO FILL THIS IN WITH YOUR PATH TO DENARII FOR THIS TO WORK SORRY
workspace_path = "/home/andrew/denarii"

# A workspace path that works if not suco on EC2
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

def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def create_build_file(libraries):
    external_dir_path = workspace_path + "/external"

    for library in libraries:

        build_file_name = "BUILD." + library.foldername

        path = os.path.join(external_dir_path, build_file_name)

        if not os.path.exists(path):
            os.mknod(path)


def create_folder(libraries):
    external_dir_path = workspace_path + "/external"

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
    create_folder(library_info)
    create_build_file(library_info)
    get_relevant_paths(library_info)
    find_includes(library_info)
    find_src_files(library_info)


def miniupnp(external_dir_path):

    # remove the empty directory
    remove_command = "rm -rf " + external_dir_path + "/miniupnp"
    os.system(remove_command)

    # For now we have to clone this because miniupnp fails to download :(
    clone_command = "git clone https://github.com/miniupnp/miniupnp.git"
    os.system(clone_command)

    # we only need to build one of the subdirectories
    miniupnp_path = external_dir_path + "/miniupnp/miniupnpc"

    os.chdir(miniupnp_path)

    command = "sudo make install"
    os.system(command)


def randomx(external_dir_path):
    randomx_path = external_dir_path + "/randomx"

    os.chdir(randomx_path)

    command = "mkdir build && cd build && cmake -DARCH=native && make"
    os.system(command)


def supercop(external_dir_path):
    os.chdir(external_dir_path)

    supercop_path = external_dir_path + "/supercop"

    supercop_zip_path = external_dir_path + "/supercop.zip"
    download_url("https://github.com/monero-project/supercop/archive/monero.zip", supercop_zip_path)

    with zipfile.ZipFile(supercop_zip_path, 'r') as zip_ref:
        zip_ref.extractall(external_dir_path)

    # for some reason there are two directories when we unzip so delete one
    delete_command = "rm -rf " + external_dir_path + "/supercop"
    os.system(delete_command)

    # we need to move the directory to the right place
    move_command = "mv " + external_dir_path + "/supercop-monero " + external_dir_path + "/supercop"
    os.system(move_command)

    os.chdir(supercop_path)

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


def unbound(external_dir_path):
    unbound_path = external_dir_path + "/unbound"

    os.chdir(unbound_path)

    command = "./configure && make && sudo make install"
    os.system(command)

    move_command = "mv /usr/local/lib/libunbound.so " + unbound_path
    os.system(move_command)


def openssl(external_dir_path):

    os.chdir(external_dir_path)

    openssl_zip_path = external_dir_path + "/openssl.zip"
    download_url("https://www.openssl.org/source/openssl-1.1.1i.tar.gz", openssl_zip_path)

    unzip_command = "tar -xvzf " + openssl_zip_path + " -C " + external_dir_path
    os.system(unzip_command)

    openssl_path = external_dir_path + "/openssl"

    openssl_wrong_name_path = external_dir_path + "/openssl-1.1.1i"
    rename_command = "mv " + openssl_wrong_name_path + " " + openssl_path
    os.system(rename_command)

    os.chdir(openssl_path)

    command = "./config && make && make test"
    os.system(command)

def libzmq(external_dir_path):
    clone_command = "git clone https://github.com/zeromq/libzmq.git"
    os.system(clone_command)

    libzmq_path = external_dir_path + "/libzmq"

    os.chdir(libzmq_path)

    command = "./autogen.sh && ./configure --with-libsodium && make && sudo make install"
    os.system(command)

    move_command = "mv /usr/local/lib/libzmq.a " + libzmq_path
    os.system(move_command)


def zlib(external_dir_path):
    zlib_path = external_dir_path + "/zlib"

    os.chdir(zlib_path)

    command = "./configure && make test && sudo make install"
    os.system(command)


def build_dependencies():
    external_dir_path = workspace_path + "/external"
    os.chdir(external_dir_path)

    miniupnp(external_dir_path)

    os.chdir(external_dir_path)
    randomx(external_dir_path)

    os.chdir(external_dir_path)
    supercop(external_dir_path)

    os.chdir(external_dir_path)
    unbound(external_dir_path)

    os.chdir(external_dir_path)
    openssl(external_dir_path)

    os.chdir(external_dir_path)
    libzmq(external_dir_path)

    os.chdir(external_dir_path)
    zlib(external_dir_path)

    os.chdir(external_dir_path)


def blocks_generate():
    input_files = ["checkpoints.dat", "stagenet_blocks.dat", "testnet_blocks.dat"]
    output_files = ["generated_checkpoints.c", "generated_stagenet_blocks.c", "generated_testnet_blocks.c"]
    base_names = ["checkpoints", "stagenet_blocks", "testnet_blocks"]

    for i in range(len(input_files)):
        input_file = input_files[i]
        output_file = output_files[i]
        base_name = base_names[i]

        path_to_blocks = workspace_path + "/src/blocks"
        command = "cd " + path_to_blocks + " && echo '#include\t<stddef.h>' > " + output_file \
                  + " && echo 'const\tunsigned\tchar\t" + base_name + "[]={' >> " + output_file + " && od -v -An -tx1 " \
                  + input_file + " | sed -e 's/[0-9a-fA-F]\\{1,\\}/0x&,/g' -e '$s/.$//' >> " + output_file + " && echo '};' >> " + output_file \
                  + " && echo 'const\tsize_t\t" + base_name + "_len\t=\tsizeof(" + base_name + ");' >> " + output_file

        os.system(command)


def crypto_wallet_generate():
    crypto_wallet_path = workspace_path + "/src/crypto/wallet"
    ops_file = "ops.h"
    build_file = "BUILD"

    supercop_path = workspace_path + "/external/supercop"
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
    else:
        # If not then we create an empty file
        command = "cd " + crypto_wallet_path + " && echo > " + ops_file
        os.system(command)
        # and create an alias for wallet that just points to cnccrypto
        alias_file_command = " cd " + crypto_wallet_path \
                             + " && echo 'package(default_visibility = [\"//visibility:public\"])\n' > " + build_file \
                             + " && echo 'alias(\n\tname = \"wallet_crypto\",\n\tactual = \"//src:cncrypto\"\n)' >> " + build_file
        os.system(alias_file_command)


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
    d = workspace_path

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

    src_directory = workspace_path + "/src/"

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

    tests_directory = workspace_path + "/tests/"

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
    translation_file_dir = workspace_path + "/translations"

    os.chdir(translation_file_dir)

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


def run_translation_generation(translation_files):
    translation_file_dir = workspace_path + "/translations"
    # create the file first
    create_command = "cd " + translation_file_dir + " && echo > translation_files.h"
    os.system(create_command)

    # need to build the binary first so the command will work
    build_command = "bazel build :generate_translations"
    os.system(build_command)

    # we cannot use bazel run because it just won't cooperate
    generation_command = workspace_path + "/bazel-bin/translations/generate_translations "

    for translation_file in translation_files:
        generation_command = generation_command + " " + translation_file

    os.system(generation_command)


def translations_generate():
    # first change all the suffixes of the translations files to .qm
    translations_files = convert_translation_files()

    # then run the generation binary with the files as arguments
    run_translation_generation(translations_files)


def generate_files():
    blocks_generate()
    crypto_wallet_generate()
    version_generate()
    benchmark_generate()
    translations_generate()


import_dependencies()
build_dependencies()
generate_files()

