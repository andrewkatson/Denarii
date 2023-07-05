workspace(name = "denarii")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "bazel_skylib",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.3.0/bazel-skylib-1.3.0.tar.gz",
    ],
    sha256 = "74d544d96f4a5bb630d465ca8bbcfe231e3594e5aae57e1edbf17a6eb3ca2506",
)
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()


# abseil-cpp
http_archive(
  name = "com_google_absl",
  urls = ["https://github.com/abseil/abseil-cpp/archive/20230125.3.zip"],
  strip_prefix = "abseil-cpp-20230125.3",
  sha256 = "51d676b6846440210da48899e4df618a357e6e44ecde7106f1e44ea16ae8adc7"
)

# Google Test
http_archive(
  name = "gtest",
  urls = ["https://github.com/google/googletest/archive/release-1.12.1.zip"],
  strip_prefix = "googletest-release-1.12.1",
  sha256 = "24564e3b712d3eb30ac9a85d92f7d720f60cc0173730ac166f27dda7fed76cb2"
)

# rules_cc defines rules for generating C++ code from Protocol Buffers.
http_archive(
    name = "rules_cc",
    sha256 = "35f2fb4ea0b3e61ad64a369de284e4fbbdcdba71836a5555abb5e194cf119509",
    strip_prefix = "rules_cc-624b5d59dfb45672d4239422fa1e3de1822ee110",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_cc/archive/624b5d59dfb45672d4239422fa1e3de1822ee110.tar.gz",
        "https://github.com/bazelbuild/rules_cc/archive/624b5d59dfb45672d4239422fa1e3de1822ee110.tar.gz",
    ],
)

# rules_java defines rules for generating Java code from Protocol Buffers.
http_archive(
    name = "rules_java",
    sha256 = "ccf00372878d141f7d5568cedc4c42ad4811ba367ea3e26bc7c43445bbc52895",
    strip_prefix = "rules_java-d7bf804c8731edd232cb061cb2a9fe003a85d8ee",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_java/archive/d7bf804c8731edd232cb061cb2a9fe003a85d8ee.tar.gz",
        "https://github.com/bazelbuild/rules_java/archive/d7bf804c8731edd232cb061cb2a9fe003a85d8ee.tar.gz",
    ],
)

# rules_proto defines abstract rules for building Protocol Buffers.
http_archive(
    name = "rules_proto",
    sha256 = "2490dca4f249b8a9a3ab07bd1ba6eca085aaf8e45a734af92aad0c42d9dc7aaf",
    strip_prefix = "rules_proto-218ffa7dfa5408492dc86c01ee637614f8695c45",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_proto/archive/218ffa7dfa5408492dc86c01ee637614f8695c45.tar.gz",
        "https://github.com/bazelbuild/rules_proto/archive/218ffa7dfa5408492dc86c01ee637614f8695c45.tar.gz",
    ],
)

# the base google protocol buffer code.
http_archive(
    name = "com_google_protobuf",
    strip_prefix = "protobuf-23.3",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v23.3.zip"],
)

# gRPC code -- has py_proto_library rule which is useful.
http_archive(
    name = "com_github_grpc_grpc",
    sha256 = "b0d3b876d85e4e4375aa211a52a33b7e8ca9f9d6d97a60c3c844070a700f0ea3",
    strip_prefix = "grpc-1.28.1",
    urls = ["https://github.com/grpc/grpc/archive/v1.28.1.zip"],
)

# proto libraries for grpc. this gives us all the esoteric languages that can be used
http_archive(
    name = "rules_proto_grpc",
    sha256 = "bbe4db93499f5c9414926e46f9e35016999a4e9f6e3522482d3760dc61011070",
    strip_prefix = "rules_proto_grpc-4.2.0",
    urls = ["https://github.com/rules-proto-grpc/rules_proto_grpc/archive/4.2.0.tar.gz"],
)

http_archive(
    name = "platforms",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/platforms/releases/download/0.0.5/platforms-0.0.5.tar.gz",
        "https://github.com/bazelbuild/platforms/releases/download/0.0.5/platforms-0.0.5.tar.gz",
    ],
    sha256 = "379113459b0feaf6bfbb584a91874c065078aa673222846ac765f86661c27407",
)

# Boost
# Famous C++ library that has given rise to many new additions to the C++ Standard Library
# Makes @boost available for use: For example, add `@boost//:algorithm` to your deps.
# For more, see https://github.com/nelhage/rules_boost and https://www.boost.org
http_archive(
    name = "com_github_nelhage_rules_boost",

    # Replace the commit hash in both places (below) with the latest, rather than using the stale one here.
    # Even better, set up Renovate and let it do the work for you (see "Suggestion: Updates" in the README).
    url = "https://github.com/nelhage/rules_boost/archive/6b7c1ce2b8d77cb6b3df6ccca0b6cf7ed13136fc.tar.gz",
    strip_prefix = "rules_boost-6b7c1ce2b8d77cb6b3df6ccca0b6cf7ed13136fc",
    sha256 = "1a3316cde21eccc337c067b21d767d252e4ac2e8041d65eb4b7b91da569c5e3f"
)

http_archive(
    name = "build_bazel_rules_nodejs",
    sha256 = "c2ad51299792d5af3b258f1dd71b3b57eff9424c2e1797d9c1d65717d95da03a",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/5.7.3/rules_nodejs-5.7.3.tar.gz"],
)

http_archive(
    name = "com_googlesource_code_re2",
    sha256 = "0a890c2aa0bb05b2ce906a15efb520d0f5ad4c7d37b8db959c43772802991887",
    strip_prefix = "re2-a427f10b9fb4622dd6d8643032600aa1b50fbd12",
    urls = ["https://github.com/google/re2/archive/a427f10b9fb4622dd6d8643032600aa1b50fbd12.zip"],  # 2022-06-09
)

# boost archive extra files
new_local_repository(
    name = "boost_extra",
    build_file = "external/BUILD.boost",
    path = "external/boost",
)

# db drivers
new_local_repository(
    name = "db_drivers",
    build_file = "external/BUILD.db_drivers",
    path = "external/db_drivers",
)

# easylogging++
new_local_repository(
    name = "easy_logging",
    build_file = "external/BUILD.easylogging++",
    path = "external/easylogging++",
)

#  miniupnp
new_local_repository(
    name = "miniupnp",
    build_file = "external/BUILD.miniupnp",
    path = "external/miniupnp",
)

#qrcodegen
new_local_repository(
    name = "qrcodegen",
    build_file = "external/BUILD.qrcodegen",
    path = "external/qrcodegen",
)

#randomx
new_local_repository(
    name = "randomx",
    build_file = "external/BUILD.randomx",
    path = "external/randomx",
)

# rapidjson
new_local_repository(
    name = "rapidjson",
    build_file = "external/BUILD.rapidjson",
    path = "external/rapidjson",
)

# supercop
new_local_repository(
    name = "supercop",
    build_file = "external/BUILD.supercop",
    path = "external/supercop",
)

# trezor-common
local_repository(
    name = "trezor_common",
    path = "external/trezor-common",
)

# unbound
new_local_repository(
    name = "unbound",
    build_file = "external/BUILD.unbound",
    path = "external/unbound",
)

# openssl
new_local_repository(
    name = "openssl",
    build_file = "external/BUILD.openssl",
    path = "external/openssl",
)

# libzmq
new_local_repository(
    name = "libzmq",
    build_file = "external/BUILD.libzmq",
    path = "external/libzmq",
)

# openpgm
new_local_repository(
    name = "openpgm",
    build_file = "external/BUILD.openpgm",
    path = "external/openpgm",
)

# expat
new_local_repository(
    name = "expat",
    build_file = "external/BUILD.expat",
    path = "external/expat",
)

# ldns
new_local_repository(
    name = "ldns",
    build_file = "external/BUILD.ldns",
    path = "external/ldns",
)

# libhidapi
new_local_repository(
    name = "libhidapi",
    build_file = "external/BUILD.libhidapi",
    path = "external/libhidapi",
)

# liblzma
new_local_repository(
    name = "liblzma",
    build_file = "external/BUILD.liblzma",
    path = "external/liblzma",
)

# libnorm
new_local_repository(
    name = "libnorm",
    build_file = "external/BUILD.libnorm",
    path = "external/libnorm",
)

# libreadline
new_local_repository(
    name = "libreadline",
    build_file = "external/BUILD.libreadline",
    path = "external/libreadline",
)

# libsodium
new_local_repository(
    name = "libsodium",
    build_file = "external/BUILD.libsodium",
    path = "external/libsodium",
)

# libudev
new_local_repository(
    name = "libudev",
    build_file = "external/BUILD.libudev",
    path = "external/libudev",
)

# libunbound
new_local_repository(
    name = "libunbound",
    build_file = "external/BUILD.libunbound",
    path = "external/libunbound",
)

# libunwind
new_local_repository(
    name = "libunwind",
    build_file = "external/BUILD.libunwind",
    path = "external/libunwind",
)

# libusb
new_local_repository(
    name = "libusb",
    build_file = "external/BUILD.libusb",
    path = "external/libusb",
)

# lrelease
new_local_repository(
    name = "lrelease",
    build_file = "external/BUILD.lrelease",
    path = "external/lrelease",
)

#zlib
new_local_repository(
    name = "zlib",
    build_file = "external/BUILD.zlib",
    path = "external/zlib",
)

#bigint
new_local_repository(
    name = "bigint",
    build_file = "external/BUILD.bigint",
    path = "external/bigint",
)

#json
new_local_repository(
    name = "json",
    build_file = "external/BUILD.json",
    path = "external/json/json",
)

#curl
new_local_repository(
    name = "curl",
    build_file = "external/BUILD.curl",
    path = "external/curl/curl",
)

load("@rules_proto_grpc//python:repositories.bzl", rules_proto_grpc_python_repos = "python_repos")

rules_proto_grpc_python_repos()

load("@rules_cc//cc:repositories.bzl", "rules_cc_dependencies")

rules_cc_dependencies()

load("@rules_java//java:repositories.bzl", "rules_java_dependencies", "rules_java_toolchains")

rules_java_dependencies()

rules_java_toolchains()

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")

rules_proto_dependencies()

rules_proto_toolchains()

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")

grpc_deps()

load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")
boost_deps()


load("@rules_proto_grpc//:repositories.bzl", "rules_proto_grpc_toolchains", "rules_proto_grpc_repos")
rules_proto_grpc_toolchains()
rules_proto_grpc_repos()

load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")
rules_proto_dependencies()
rules_proto_toolchains()

load("@build_bazel_rules_nodejs//:repositories.bzl", "build_bazel_rules_nodejs_dependencies")

build_bazel_rules_nodejs_dependencies()

