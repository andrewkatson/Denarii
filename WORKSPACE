workspace(name = "denarii")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

register_execution_platforms(
  ":x64_windows-clang-cl"
)

register_toolchains(
  "@local_config_cc//:cc-toolchain-x64_windows-clang-cl",
)

# abseil-cpp
http_archive(
    name = "com_google_absl",
    sha256 = "8400c511d64eb4d26f92c5ec72535ebd0f843067515244e8b50817b0786427f9",
    strip_prefix = "abseil-cpp-c512f118dde6ffd51cb7d8ac8804bbaf4d266c3a",
    urls = ["https://github.com/abseil/abseil-cpp/archive/c512f118dde6ffd51cb7d8ac8804bbaf4d266c3a.zip"],
)

# Google Test
http_archive(
    name = "gtest",
    sha256 = "94c634d499558a76fa649edb13721dce6e98fb1e7018dfaeba3cd7a083945e91",
    strip_prefix = "googletest-release-1.10.0",
    url = "https://github.com/google/googletest/archive/release-1.10.0.zip",
)

# C++ protocol buffer rules for Bazel.
http_archive(
    name = "rules_cc",
    sha256 = "954b7a3efc8752da957ae193a13b9133da227bdacf5ceb111f2e11264f7e8c95",
    strip_prefix = "rules_cc-9e10b8a6db775b1ecd358d8ddd3dab379a2c29a5",
    urls = ["https://github.com/bazelbuild/rules_cc/archive/9e10b8a6db775b1ecd358d8ddd3dab379a2c29a5.zip"],
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
    sha256 = "602e7161d9195e50246177e7c55b2f39950a9cf7366f74ed5f22fd45750cd208",
    strip_prefix = "rules_proto-97d8af4dc474595af3900dd85cb3a29ad28cc313",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
        "https://github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
    ],
)

# language specific rules for building python with Bazel.
http_archive(
    name = "rules_python",
    sha256 = "e5470e92a18aa51830db99a4d9c492cc613761d5bdb7131c04bd92b9834380f6",
    strip_prefix = "rules_python-4b84ad270387a7c439ebdccfd530e2339601ef27",
    urls = ["https://github.com/bazelbuild/rules_python/archive/4b84ad270387a7c439ebdccfd530e2339601ef27.tar.gz"],
)

# the base google protocol buffer code.
http_archive(
    name = "com_google_protobuf",
    sha256 = "60d2012e3922e429294d3a4ac31f336016514a91e5a63fd33f35743ccfe1bd7d",
    strip_prefix = "protobuf-3.11.0",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/v3.11.0.zip"],
)

# gRPC code -- has py_proto_library rule which is useful.
http_archive(
    name = "com_github_grpc_grpc",
    sha256 = "b0d3b876d85e4e4375aa211a52a33b7e8ca9f9d6d97a60c3c844070a700f0ea3",
    strip_prefix = "grpc-1.28.1",
    urls = ["https://github.com/grpc/grpc/archive/v1.28.1.zip"],
)

# boost
git_repository(
    name = "com_github_nelhage_rules_boost",
    commit = "1e3a69bf2d5cd10c34b74f066054cd335d033d71",
    remote = "https://github.com/nelhage/rules_boost",
    shallow_since = "1591047380 -0700",
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

#keiros public
local_repository(
    name = "keiros_public",
    path = "external/KeirosPublic",
)

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
