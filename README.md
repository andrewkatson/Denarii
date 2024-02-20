# Denarii

Copyright (c) 2020-2023 Denarii.   
Portions Copyright (c) 2014-2020 The Monero Project.   
Portions Copyright (c) 2012-2013 The Cryptonote developers.

## Table of Contents

  - [Introduction](#introduction)
  - [License](#license)
  - [Compiling Denarii from source](#compiling-denarii-from-source)
    - [Dependencies](#dependencies)
  - [Configuration Instructions](#configuration-instructions)
  - [Building](#building)
  - [Running Denariid](#running-denariid)
  - [Running Denarii Wallet Rpc Server](#running-denarii-wallet-rpc-server)
  - [Running Denarii GUI](#running-denarii-gui)
  - [Internationalization](#Internationalization)
  - [Using Tor](#using-tor)
  - [Pruning](#Pruning)
  - [Debugging](#Debugging)
  - [Known issues](#known-issues)
  
## Introduction

Denarii is a private, secure, untraceable, decentralised digital currency. You are your bank, you control your funds, and nobody can trace your transfers unless you allow them to do so.

**Privacy:** Denarii uses a cryptographically sound system to allow you to send and receive funds without your transactions being easily revealed on the blockchain (the ledger of transactions that everyone has). This ensures that your purchases, receipts, and all transfers remain absolutely private by default.

**Security:** Using the power of a distributed peer-to-peer consensus network, every transaction on the network is cryptographically secured. Individual wallets have a 25-word mnemonic seed that is only displayed once and can be written down to backup the wallet. Wallet files are encrypted with a passphrase to ensure they are useless if stolen.

**Untraceability:** By taking advantage of ring signatures, a special property of a certain type of cryptography, Denarii is able to ensure that transactions are not only untraceable but have an optional measure of ambiguity that ensures that transactions cannot easily be tied back to an individual user or computer.

**Decentralization:** The utility of Denarii depends on its decentralised peer-to-peer consensus network - anyone should be able to run the denarii software, validate the integrity of the blockchain, and participate in all aspects of the denarii network using consumer-grade commodity hardware. Decentralization of the monero network is maintained by software development that minimizes the costs of running the denarii software and inhibits the proliferation of specialized, non-commodity hardware.  

**Stability:** Denarii is a stable currency through the adoption of proven modern monetary policy modified to be decentralized. Essentially it manages the emission rate and the transaction fee to react to the market over time. This is done through the adjustment of these critical values by the nodes of the network -- but restricted by the average of the previous n blocks.

## License

See [LICENSE](LICENSE).

## Compiling Denarii from source

### Note
* Everything has to be built with sudo because the files are moved using sudo and that gives them certain permissions.
* The real dependencies no longer need to be fiddled with just run the configuration script and it will do the rest.
* Need to set an enviornment variable ```DENARI_WORKSPACE_PATH=``` and then put whatever the path is to folder containing the ```WORKSPACE``` file. 

### Dependencies

The following table summarizes the tools and libraries required to build. A
few of the libraries are also included in this repository (marked as
"Vendored"). By default, the build uses the library installed on the system
and ignores the vendored sources. However, if no library is found installed on
the system, then the vendored source will be built and used. The vendored
sources are also used for statically-linked builds because distribution
packages often include only shared library binaries (`.so`) but not static
library archives (`.a`).

| Dep          | Min. version  | Vendored | Debian/Ubuntu pkg    | Arch pkg     | Void pkg           | Fedora pkg          | Optional | Purpose         |
| ------------ | ------------- | -------- | -------------------- | ------------ | ------------------ | ------------------- | -------- | --------------- |
| GCC          | 4.7.3         | NO       | `build-essential`    | `base-devel` | `base-devel`       | `gcc`               | NO       |                 |
| CMake        | 3.5           | NO       | `cmake`              | `cmake`      | `cmake`            | `cmake`             | NO       |                 |
| pkg-config   | any           | NO       | `pkg-config`         | `base-devel` | `base-devel`       | `pkgconf`           | NO       |                 |
| Boost        | 1.58          | NO       | `libboost-all-dev`   | `boost`      | `boost-devel`      | `boost-devel`       | NO       | C++ libraries   |
| OpenSSL      | basically any | NO       | `libssl-dev`         | `openssl`    | `libressl-devel`   | `openssl-devel`     | NO       | sha256 sum      |
| libzmq       | 3.0.0         | NO       | `libzmq3-dev`        | `zeromq`     | `zeromq-devel`     | `zeromq-devel`      | NO       | ZeroMQ library  |
| OpenPGM      | ?             | NO       | `libpgm-dev`         | `libpgm`     |                    | `openpgm-devel`     | NO       | For ZeroMQ      |
| libnorm[2]   | ?             | NO       | `libnorm-dev`        |              |                    |                     | YES      | For ZeroMQ      |
| libunbound   | 1.4.16        | YES      | `libunbound-dev`     | `unbound`    | `unbound-devel`    | `unbound-devel`     | NO       | DNS resolver    |
| libsodium    | ?             | NO       | `libsodium-dev`      | `libsodium`  | `libsodium-devel`  | `libsodium-devel`   | NO       | cryptography    |
| libunwind    | any           | NO       | `libunwind8-dev`     | `libunwind`  | `libunwind-devel`  | `libunwind-devel`   | YES      | Stack traces    |
| liblzma      | any           | NO       | `liblzma-dev`        | `xz`         | `liblzma-devel`    | `xz-devel`          | YES      | For libunwind   |
| libreadline  | 6.3.0         | NO       | `libreadline6-dev`   | `readline`   | `readline-devel`   | `readline-devel`    | YES      | Input editing   |
| ldns         | 1.6.17        | NO       | `libldns-dev`        | `ldns`       | `libldns-devel`    | `ldns-devel`        | YES      | SSL toolkit     |
| expat        | 1.1           | NO       | `libexpat1-dev`      | `expat`      | `expat-devel`      | `expat-devel`       | YES      | XML parsing     |
| GTest        | 1.5           | YES      | `libgtest-dev`[1]    | `gtest`      | `gtest-devel`      | `gtest-devel`       | YES      | Test suite      |
| Doxygen      | any           | NO       | `doxygen`            | `doxygen`    | `doxygen`          | `doxygen`           | YES      | Documentation   |
| Graphviz     | any           | NO       | `graphviz`           | `graphviz`   | `graphviz`         | `graphviz`          | YES      | Documentation   |
| lrelease     | ?             | NO       | `qttools5-dev-tools` | `qt5-tools`  | `qt5-tools`        | `qt5-linguist`      | YES      | Translations    |
| libhidapi    | ?             | NO       | `libhidapi-dev`      | `hidapi`     | `hidapi-devel`     | `hidapi-devel`      | YES      | Hardware wallet |
| libusb       | ?             | NO       | `libusb-1.0-0-dev`   | `libusb`     | `libusb-devel`     | `libusbx-devel`     | YES      | Hardware wallet |
| libprotobuf  | ?             | NO       | `libprotobuf-dev`    | `protobuf`   | `protobuf-devel`   | `protobuf-devel`    | YES      | Hardware wallet |
| protoc       | ?             | NO       | `protobuf-compiler`  | `protobuf`   | `protobuf`         | `protobuf-compiler` | YES      | Hardware wallet |
| libudev      | ?             | No       | `libudev-dev`        | `systemd`    | `eudev-libudev-devel` | `systemd-devel`     | YES      | Hardware wallet |

[1] On Debian/Ubuntu `libgtest-dev` only includes sources and headers. You must
build the library binary manually. This can be done with the following command ```sudo apt-get install libgtest-dev && cd /usr/src/gtest && sudo cmake . && sudo make && sudo mv libg* /usr/lib/ ```
[2] libnorm-dev is needed if your zmq library was built with libnorm, and not needed otherwise

Install all dependencies at once on Debian/Ubuntu:

```sudo apt update && sudo apt install build-essential cmake pkg-config libboost-all-dev libssl-dev libzmq3-dev libunbound-dev libsodium-dev libunwind8-dev liblzma-dev libreadline6-dev libldns-dev libexpat1-dev doxygen graphviz libpgm-dev qttools5-dev-tools libhidapi-dev libusb-1.0-0-dev libprotobuf-dev protobuf-compiler libudev-dev libnorm-dev  qtbase5-dev qt5-qmake python-pip && sudo apt-get install python3-pyqt5```

Install all dependencies at once on macOS with the provided Brewfile:
```brew update && brew bundle --file=contrib/brew/Brewfile && pip3 install PyQt5 ```

FreeBSD 12.1 one-liner required to build dependencies:
```pkg install git gmake cmake pkgconf boost-libs libzmq4 libsodium```

### Cloning the repository

Clone recursively to pull-in needed submodule(s):

`$ git clone --recursive git@github.com:andrewkatson/denarii.git`

If you already have a repo cloned, initialize and update:

`$ cd denarii && git submodule init && git submodule update`

## Configuration instructions

Denarii uses bazel (https://bazel.build/). And it needs `C++14` at least. So set `BAZEL_CXXOPTS="-std=c++14"` on Linux/Mac and `BAZEL_CXXOPT="-std:c++14"` on Windows.

### On Linux and macOS

* Install the dependencies
* Change to the root of the source code directory, change to the most recent release branch, and build:

    ```bash
    cd denarii
    git checkout release-v0.17
    sudo bazel run :configure
    sudo chmod -R 777 /path/to/denarii
    ```

### On Windows
* Download and install the following. Make sure they are in your path.
CMAKE: https://cmake.org/download/
Make: http://gnuwin32.sourceforge.net/packages/make.htm
MinGW: https://sourceforge.net/projects/mingw/files/latest/download
Msys2: https://www.msys2.org/
Bazel with gcc: https://github.com/bazelbuild/bazel/issues/12100
Visual Studio: https://visualstudio.microsoft.com/

* Open the MSYS shell via the `MSYS2 Shell` shortcut
* Update packages using pacman:  

    ```bash
    pacman -Syu
    ```

* Exit the MSYS shell using Alt+F4  
* Edit the properties for the `MSYS2 Shell` shortcut changing "msys2_shell.bat" to "msys2_shell.cmd -mingw64" for 64-bit builds or "msys2_shell.cmd -mingw32" for 32-bit builds. 
  You could also just open the msys of the appropriate type found under ```C:/Users/%USER%/AppData/Roaming/Micorsoft/Windwos/'Start Menu'/Programs/'Msys 64bit'```
* Restart MSYS shell via modified shortcut and update packages again using pacman:  

    ```bash
    pacman -Syu
    ```


* Install dependencies:

    To build for 64-bit Windows in Msys2:

    ```bash
    pacman -S mingw-w64-x86_64-toolchain make mingw-w64-x86_64-cmake mingw-w64-x86_64-boost mingw-w64-x86_64-openssl mingw-w64-x86_64-zeromq mingw-w64-x86_64-libsodium mingw-w64-x86_64-hidapi mingw-w64-x86_64-libunwind mingw-w64-x86_64-libusb mingw-w64-x86_64-unbound mingw-w64-x86_64-lmdb mingw-w64-x86_64-qt-creator mingw-w64-x86_64-python-pyqt5 mingw-w64-x86_64-qt5-tools
    ```

    To build for 32-bit Windows in Msys2:

    ```bash
    pacman -S mingw-w64-i686-toolchain make mingw-w64-i686-cmake mingw-w64-i686-boost mingw-w64-i686-openssl mingw-w64-i686-zeromq mingw-w64-i686-libsodium mingw-w64-i686-hidapi mingw-w64-i686-libunwind mingw-w64-i686-libusb mingw-w64-i686-unbound mingw-w64-i686-lmdb mingw-w64-i686-qt-creator mingw-w64-i686-python-pyqt5 mingw-w64-i686-qt5-tools
    ```
  
    Then run in command prompt 
    ```bash 
    pip install PyQt5
    ```
  
* Run Configure 

    ``` 
    bazel run :configure_win (run through command prompt)
    bazel run :configure     (run through msys2) or python configure.py (run through msys2)
    ```

## Building 

### On Linux 


Do `bazel build target` for all targets -- e.g. ```bazel build src:denariid```


### On Windows  

All builds should use ```--compiler=mingw-gcc --copt="-O3" --copt="-DWIN32_LEAN_AND_MEAN" --copt="-DMINIUPNP_STATICLIB" --copt="-DZMQ_STATIC" --linkopt="-static"```

If you want to build in debug mode use `--compilation_mode=dbg` instead of `--copt="-O3"` and also add in `--linkopt="mcmodel=medium"` and `--copt="=Wa,-mbig-obj"`

Need to set JAVA_HOME in msys. Mine is ```export JAVA_HOME=/c/'Program Files'/Java/jdk-10.0.2```

Protoc works weird with mingw-gcc so you have to fix it.

Add the following files to `C:\msys64\mingw-gcc\bin`
* `ntdll.dll`
* `KERNEL32.DLL`
* `KERNELBASE.dll`
* `msvcrt.dll` 

These can all be found under `C:\Windows\SYSTEM32` 

### On Mac

Do `bazel build target` on all targets.

## Running denariid

### On Linux

The build places the binary in `bazel-bin/` sub-directory. To run in the
foreground:

```bash
./bazel-bin/src/denariid
```

To list all available options, run `./bazel-bin/src/denariid--help`.  Options can be
specified either on the command line or in a configuration file passed by the
`--config-file` argument.  To specify an option in the configuration file, add
a line with the syntax `argumentname=value`, where `argumentname` is the name
of the argument without the leading dashes, for example, `log-level=1`.

To run in background:

```bash
./bazel-bin/src/denariid --log-file denariid.log --detach
```

### On Windows 
```bash
start bazel-bin/src/denariid.exe
```

### On Mac
```bash
./bazel-bin/src/denariid
```

If you're on Mac, you may need to add the `--max-concurrency 1` option to
denarii-wallet-cli, and possibly denariid, if you get crashes refreshing. You also might need `--no-igd`.

## Running denarii wallet rpc server

### On Linux

The build places the binary in `bazel-bin` sub-directory: To run in the foreground: 

```bash
sudo ./bazel-bin/src/denarii_wallet_rpc_server --rpc-bind-port=8080 --wallet-dir=/some/existing/path
```

### On Windows 

```bash 
start bazel-bin/src/denarii_wallet_rpc_server.exe --rpc-bind-port=8080 --wallet-dir=/some/existing/path
```

## Testing 

Set the path to this workspace in `contrib/epee/include/string_tools.h` in function `get_workspace_path`. And set it in `tests/unit_tests/BUILD`.

Run 
```bash 
bazel run tests:get_monero_test_commands
```

Then execute the command it prints out.

#### Stack Traces on Windows 

Linux has stack traces by default. Windows crashes when there is a stack trace so we by default do not log them. However, you can enable them with `--copt="-DSTACK_TRACE_DENARII`

### On Mac

```bash
./bazel-bin/src/denarii_wallet_rpc_server --rpc-bind-port=8080 --wallet-dir=/some/existing/path
```

## Running Denarii GUI

See `./utils/gui/README.md` for details.

## Internationalization

See [README.i18n.md](README.i18n.md).

## Using Tor

> There is a new, still experimental, [integration with Tor](ANONYMITY_NETWORKS.md). The
> feature allows connecting over IPv4 and Tor simultaneously - IPv4 is used for
> relaying blocks and relaying transactions received by peers whereas Tor is
> used solely for relaying transactions received over local RPC. This provides
> privacy and better protection against surrounding node (sybil) attacks.

While Denarii isn't made to integrate with Tor, it can be used wrapped with torsocks, by
setting the following configuration parameters and environment variables:

* `--p2p-bind-ip 127.0.0.1` on the command line or `p2p-bind-ip=127.0.0.1` in
  monerod.conf to disable listening for connections on external interfaces.
* `--no-igd` on the command line or `no-igd=1` in monerod.conf to disable IGD
  (UPnP port forwarding negotiation), which is pointless with Tor.
* `DNS_PUBLIC=tcp` or `DNS_PUBLIC=tcp://x.x.x.x` where x.x.x.x is the IP of the
  desired DNS server, for DNS requests to go over TCP, so that they are routed
  through Tor. When IP is not specified, denariid uses the default list of
  servers defined in [src/common/dns_utils.cpp](src/common/dns_utils.cpp).
* `TORSOCKS_ALLOW_INBOUND=1` to tell torsocks to allow denariid to bind to interfaces
   to accept connections from the wallet. On some Linux systems, torsocks
   allows binding to localhost by default, so setting this variable is only
   necessary to allow binding to local LAN/VPN interfaces to allow wallets to
   connect from remote hosts. On other systems, it may be needed for local wallets
   as well.
* Do NOT pass `--detach` when running through torsocks with systemd, (see
  [utils/systemd/monerod.service](utils/systemd/monerod.service) for details).
* If you use the wallet with a Tor daemon via the loopback IP (eg, 127.0.0.1:9050),
  then use `--untrusted-daemon` unless it is your own hidden service.

Example command line to start denariid through Tor:

```bash
DNS_PUBLIC=tcp torsocks ./bazel-bin/src/denariid --p2p-bind-ip 127.0.0.1 --no-igd
```

### Using Tor on Tails

TAILS ships with a very restrictive set of firewall rules. Therefore, you need
to add a rule to allow this connection too, in addition to telling torsocks to
allow inbound connections. Full example:

```bash
sudo iptables -I OUTPUT 2 -p tcp -d 127.0.0.1 -m tcp --dport 18081 -j ACCEPT
DNS_PUBLIC=tcp torsocks ./bazel-bin/src/denariid --p2p-bind-ip 127.0.0.1 --no-igd --rpc-bind-ip 127.0.0.1 \
    --data-dir /home/amnesia/Persistent/your/directory/to/the/blockchain
```

## Pruning
One can store a pruned blockchain,  which is ~1/3 the size of the full chain.
A pruned blockchain can only serve part of the historical chain data to other peers, but is otherwise identical in
functionality to the full blockchain.
To use a pruned blockchain, it is best to start the initial sync with --prune-blockchain. However, it is also possible
to prune an existing blockchain using the denarii-blockchain-prune tool or using the --prune-blockchain denariid option
with an existing chain. If an existing chain exists, pruning will temporarily require disk space to store both the full
and pruned blockchains.

## Debugging

This section contains general instructions for debugging failed installs or problems encountered with Denarii. First, ensure you are running the latest version built from the Github repo.

### Obtaining stack traces and core dumps on Unix systems

We generally use the tool `gdb` (GNU debugger) to provide stack trace functionality, and `ulimit` to provide core dumps in builds which crash or segfault. You need to use version 10+.

* To use `gdb` in order to obtain a stack trace for a build that has stalled:

Run the build.

Once it stalls, enter the following command:

```bash
gdb /path/to/denaridd `pidof denariid`
```

Type `thread apply all bt` within gdb in order to obtain the stack trace

* If however the core dumps or segfaults:

Enter `ulimit -c unlimited` on the command line to enable unlimited filesizes for core dumps

Enter `echo core | sudo tee /proc/sys/kernel/core_pattern` to stop cores from being hijacked by other tools

Run the build.

When it terminates with an output along the lines of "Segmentation fault (core dumped)", there should be a core dump file in the same directory as denariid. It may be named just `core`, or `core.xxxx` with numbers appended.

You can now analyse this core dump with `gdb` as follows:

```bash
gdb /path/to/denariid /path/to/dumpfile`
```

Print the stack trace with `bt`

 * If a program crashed and cores are managed by systemd, the following can also get a stack trace for that crash:

```bash
coredumpctl -1 gdb
```

#### To run Denarii within gdb:

Type `gdb /path/to/denaridd` but you will need to follow the instructions here https://stackoverflow.com/questions/71903316/gdb-command-aborted-for-all-commands?noredirect=1#comment127059480_71903316 and get the latest gdb.

Pass command-line options with `--args` followed by the relevant arguments

Type `run` to run denariid

### Analysing memory corruption

There are two tools available:

#### ASAN

Configure Denarii with the -D SANITIZE=ON cmake flag, eg:

```bash
cd build/debug && cmake -D SANITIZE=ON -D CMAKE_BUILD_TYPE=Debug ../..
```

You can then run the Denarii tools normally. Performance will typically halve.

#### valgrind

Install valgrind and run as `valgrind /path/to/denariid`. It will be very slow.

### LMDB

Instructions for debugging suspected blockchain corruption as per @HYC

There is an `mdb_stat` command in the LMDB source that can print statistics about the database but it's not routinely built. This can be built with the following command:

```bash
cd ~/denarii/external/db_drivers/liblmdb && make
```

The output of `mdb_stat -ea <path to blockchain dir>` will indicate inconsistencies in the blocks, block_heights and block_info table.

The output of `mdb_dump -s blocks <path to blockchain dir>` and `mdb_dump -s block_info <path to blockchain dir>` is useful for indicating whether blocks and block_info contain the same keys.

These records are dumped as hex data, where the first line is the key and the second line is the data.

## Known Issues

### Building 

#### Mac 

Only works with `ARM` CPUs.

#### Windows 

Only works with `x86` CPUs.

#### Linux 

Only works on `Ubuntu` with `x86` CPUs.

### Protocols

#### Socket-based

Because of the nature of the socket-based protocols that drive denarii, certain protocol weaknesses are somewhat unavoidable at this time. While these weaknesses can theoretically be fully mitigated, the effort required (the means) may not justify the ends. As such, please consider taking the following precautions if you are a denarii node operator:

- Run `denariid` on a "secured" machine. If operational security is not your forte, at a very minimum, have a dedicated a computer running `denariid` and **do not** browse the web, use email clients, or use any other potentially harmful apps on your `denariid` machine. **Do not click links or load URL/MUA content on the same machine**. Doing so may potentially exploit weaknesses in commands which accept "localhost" and "127.0.0.1".
- If you plan on hosting a public "remote" node, start `denariid` with `--restricted-rpc`. This is a must.

#### Blockchain-based

Certain blockchain "features" can be considered "bugs" if misused correctly. Consequently, please consider the following:

- When receiving denarii, be aware that it may be locked for an arbitrary time if the sender elected to, preventing you from spending that denarii until the lock time expires. You may want to hold off acting upon such a transaction until the unlock time lapses. To get a sense of that time, you can consider the remaining blocktime until unlock as seen in the `show_transfers` command.

### Connections 

#### Denariid on Windows 

- Right now, `denaiid.exe` will sometimes fail to connect to the network. If it happens just restart it. The gui will restart it automatically in the background.