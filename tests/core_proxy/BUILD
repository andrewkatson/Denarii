package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "core_proxy",
    srcs = [
        "core_proxy.cpp",
        "core_proxy.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-W",
        "-Bdynamic",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:p2p",
        "//src:version",
        "@easy_logging",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)
