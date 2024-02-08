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
        ]
    }) + [
        "-lreadline",
    ],
    deps = [
        "//src:cncrypto",
        "//src:cryptonote_basic",
        "@liblzma",
        "@libnorm",
        "@libreadline",
        "@libzmq",
        "@openpgm",
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
        "//src:cncrypto",
        "//src:cryptonote_basic",
        "@liblzma",
        "@libreadline",
    ],
)

py_binary(
    name = "run_monero_tests",
    srcs = ["run_monero_tests.py"],
    deps = ["//:workspace_path_finder"],
    imports = ["//:workspace_path_finder"]
)

py_binary(
    name = "get_monero_test_commands",
    srcs = ["get_monero_test_commands.py"],
    deps = ["//:workspace_path_finder"],
    imports = ["//:workspace_path_finder"]
)
