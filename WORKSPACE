workspace(name = "denarii")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "bazel_skylib",
    sha256 = "cd55a062e763b9349921f0f5db8c3933288dc8ba4f76dd9416aac68acee3cb94",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.5.0/bazel-skylib-1.5.0.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.5.0/bazel-skylib-1.5.0.tar.gz",
    ],
)
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")

bazel_skylib_workspace()

# Allows  us to check which features are available
http_archive(
    name = "bazel_features",
    sha256 = "0f23d75c7623d6dba1fd30513a94860447de87c8824570521fcc966eda3151c2",
    strip_prefix = "bazel_features-1.4.1",
    url = "https://github.com/bazel-contrib/bazel_features/releases/download/v1.4.1/bazel_features-v1.4.1.tar.gz",
)
load("@bazel_features//:deps.bzl", "bazel_features_deps")
bazel_features_deps()

http_archive(
    name = "platforms",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/platforms/releases/download/0.0.8/platforms-0.0.8.tar.gz",
        "https://github.com/bazelbuild/platforms/releases/download/0.0.8/platforms-0.0.8.tar.gz",
    ],
    sha256 = "8150406605389ececb6da07cbcb509d5637a3ab9a24bc69b1101531367d89d74",
)

http_archive(
    name = "bazel_skylib_gazelle_plugin",
    sha256 = "747addf3f508186234f6232674dd7786743efb8c68619aece5fb0cac97b8f415",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.5.0/bazel-skylib-gazelle-plugin-1.5.0.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.5.0/bazel-skylib-gazelle-plugin-1.5.0.tar.gz",
    ],
)

# Boost
# Famous C++ library that has given rise to many new additions to the C++ Standard Library
# Makes @boost available for use: For example, add `@boost//:algorithm` to your deps.
# For more, see https://github.com/nelhage/rules_boost and https://www.boost.org
http_archive(
    name = "com_github_nelhage_rules_boost",

    # Replace the commit hash in both places (below) with the latest, rather than using the stale one here.
    # Even better, set up Renovate and let it do the work for you (see "Suggestion: Updates" in the README).
    url = "https://github.com/nelhage/rules_boost/archive/98bdaa9155c32a9b7aed15a2e6c33c90a2f6840c.tar.gz",
    strip_prefix = "rules_boost-98bdaa9155c32a9b7aed15a2e6c33c90a2f6840c",
    integrity = "sha256-MejlbKWZotRlbWnm3lLaWmMHlwjZBVHbnY8yGl9QT5M="
)

http_archive(
    name = "com_googlesource_code_re2",
    strip_prefix = "re2-2024-02-01",
    urls = ["https://github.com/google/re2/archive/2024-02-01.zip"],  # 2024-02-01
)

# boost archive extra files
new_local_repository(
    name = "boost_extra",
    build_file = "@//external:BUILD.boost",
    path = "external/boost",
)

# db drivers
new_local_repository(
    name = "db_drivers",
    build_file = "@//external:BUILD.db_drivers",
    path = "external/db_drivers",
)

# easylogging++
new_local_repository(
    name = "easy_logging",
    build_file = "@//external:BUILD.easylogging++",
    path = "external/easylogging++",
)

#  miniupnp
new_local_repository(
    name = "miniupnp",
    build_file = "@//external:BUILD.miniupnp",
    path = "external/miniupnp",
)

#qrcodegen
new_local_repository(
    name = "qrcodegen",
    build_file = "@//external:BUILD.qrcodegen",
    path = "external/qrcodegen",
)

#randomx
new_local_repository(
    name = "randomx",
    build_file = "@//external:BUILD.randomx",
    path = "external/randomx",
)

# rapidjson
new_local_repository(
    name = "rapidjson",
    build_file = "@//external:BUILD.rapidjson",
    path = "external/rapidjson",
)

# supercop
new_local_repository(
    name = "supercop",
    build_file = "@//external:BUILD.supercop",
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
    build_file = "@//external:BUILD.unbound",
    path = "external/unbound",
)

# openssl
new_local_repository(
    name = "openssl",
    build_file = "@//external:BUILD.openssl",
    path = "external/openssl",
)

# libzmq
new_local_repository(
    name = "libzmq",
    build_file = "@//external:BUILD.libzmq",
    path = "external/libzmq",
)

# openpgm
new_local_repository(
    name = "openpgm",
    build_file = "@//external:BUILD.openpgm",
    path = "external/openpgm",
)

# expat
new_local_repository(
    name = "expat",
    build_file = "@//external:BUILD.expat",
    path = "external/expat",
)

# ldns
new_local_repository(
    name = "ldns",
    build_file = "@//external:BUILD.ldns",
    path = "external/ldns",
)

# libhidapi
new_local_repository(
    name = "libhidapi",
    build_file = "@//external:BUILD.libhidapi",
    path = "external/libhidapi",
)

# liblzma
new_local_repository(
    name = "liblzma",
    build_file = "@//external:BUILD.liblzma",
    path = "external/liblzma",
)

# libnorm
new_local_repository(
    name = "libnorm",
    build_file = "@//external:BUILD.libnorm",
    path = "external/libnorm",
)

# libreadline
new_local_repository(
    name = "libreadline",
    build_file = "@//external:BUILD.libreadline",
    path = "external/libreadline",
)

# libsodium
new_local_repository(
    name = "libsodium",
    build_file = "@//external:BUILD.libsodium",
    path = "external/libsodium",
)

# libudev
new_local_repository(
    name = "libudev",
    build_file = "@//external:BUILD.libudev",
    path = "external/libudev",
)

# libunbound
new_local_repository(
    name = "libunbound",
    build_file = "@//external:BUILD.libunbound",
    path = "external/libunbound",
)

# libunwind
new_local_repository(
    name = "libunwind",
    build_file = "@//external:BUILD.libunwind",
    path = "external/libunwind",
)

# libusb
new_local_repository(
    name = "libusb",
    build_file = "@//external:BUILD.libusb",
    path = "external/libusb",
)

# lrelease
new_local_repository(
    name = "lrelease",
    build_file = "@//external:BUILD.lrelease",
    path = "external/lrelease",
)

#zlib
new_local_repository(
    name = "zlib",
    build_file = "@//external:BUILD.zlib",
    path = "external/zlib",
)

#bigint
new_local_repository(
    name = "bigint",
    build_file = "@//external:BUILD.bigint",
    path = "external/bigint",
)

#json
new_local_repository(
    name = "json",
    build_file = "@//external:BUILD.json",
    path = "external/json/json",
)

#curl
new_local_repository(
    name = "curl",
    build_file = "@//external:BUILD.curl",
    path = "external/curl/curl",
)

load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")

boost_deps()

load("@bazel_skylib_gazelle_plugin//:workspace.bzl", "bazel_skylib_gazelle_plugin_workspace")

bazel_skylib_gazelle_plugin_workspace()

load("@bazel_skylib_gazelle_plugin//:setup.bzl", "bazel_skylib_gazelle_plugin_setup")

bazel_skylib_gazelle_plugin_setup()