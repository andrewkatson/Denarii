package(default_visibility = ["//visibility:public"])

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
    ],
    deps = [
        "//contrib/epee",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:version",
        "//src:wallet",
        "//src/multisig",
        "@liblzma",
        "@libreadline",
        "@libunwind",
        "@libzmq",
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
        "//src/multisig",
        "@liblzma",
        "@libreadline",
        "@libunwind",
        "@libzmq",
    ],
)
