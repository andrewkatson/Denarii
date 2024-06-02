package(default_visibility = ["//visibility:public"])

config_setting(
    name="windows",
    constraint_values=[
        "@platforms//os:windows",
    ],
    visibility=["//visibility:public"],
)

config_setting(
    name = "mac",
    constraint_values=[
        "@platforms//os:macos",
    ],
    visibility=["//visibility:public"],
)

config_setting(
   name = "linux",
   constraint_values = [
      "@platforms//os:linux",
   ],
   visibility = ["//visibility:public"],
)

cc_binary(
    name = "core_tests",
    srcs = glob([
        "*.h",
        "*.inl",
    ]) + glob(["*.cpp"]),
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lsodium",
        "-lunwind",
        "-llzma",
    ] + select({
        'linux': ["-fPIC",],
        'windows': ["-fPIC",],
        'mac': []
    }),
    deps = [
        "//contrib/epee",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:version",
        "//src:wallet",
        "//src:multisig",
        "@denarii_external//:liblzma",
        "@denarii_external//:libreadline",
        "@denarii_external//:libunwind",
        "@denarii_external//:libzmq",
    ],
)

cc_library(
    name = "tools",
    srcs = [
        "chaingen.cpp",
        "wallet_tools.cpp",
    ],
    hdrs = [
        "chaingen.h",
        "wallet_tools.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lsodium",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:version",
        "//src:wallet",
        "//src:multisig",
        "@denarii_external//:liblzma",
        "@denarii_external//:libreadline",
        "@denarii_external//:libunwind",
        "@denarii_external//:libzmq",
    ],
)
