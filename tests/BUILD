package(default_visibility = ["//visibility:public"])

config_setting(
    name = "windows",
    constraint_values = [
        "@platforms//os:windows",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "mac",
    constraint_values = [
        "@platforms//os:macos",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "linux",
    constraint_values = [
        "@platforms//os:linux",
    ],
    visibility = ["//visibility:public"],
)

# Doesn't build on MacOS because it tries to evaluate @libnorm and recurs endlessly.
cc_binary(
    name = "benchmark",
    srcs = [
        "benchmark.cpp",
        "benchmark.h",
    ],
    linkopts = select({
        "windows": [],
        "mac": [],
        "linux": [
            "-ltinfo",
            "-lnorm",
        ],
    }) + [
        "-lreadline",
    ],
    deps = [
        "//other:liblzma",
        "//other:libnorm",
        "//other:libreadline",
        "//other:libzmq",
        "//other:openpgm",
        "//src:cncrypto",
        "//src:cryptonote_basic",
        "@supercop//:supercop51",
        "@supercop//:supercop64",
    ],
)

cc_library(
    name = "io",
    srcs = [],
    hdrs = ["io.h"],
    deps = [],
)

cc_binary(
    name = "hash_tests",
    srcs = ["hash-target.cpp"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//contrib/epee",
        "//other:liblzma",
        "//other:libreadline",
        "//src:cncrypto",
        "//src:cryptonote_basic",
    ],
)

py_binary(
    name = "run_monero_tests",
    srcs = ["run_monero_tests.py"],
    imports = ["//:workspace_path_finder"],
    deps = ["//:workspace_path_finder"],
)

py_binary(
    name = "get_monero_test_commands",
    srcs = ["get_monero_test_commands.py"],
    imports = ["//:workspace_path_finder"],
    deps = ["//:workspace_path_finder"],
)
