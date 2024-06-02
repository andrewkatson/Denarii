package(default_visibility = ["//visibility:public"])

cc_test(
    name = "performance_tests",
    srcs = ["main.cpp"] + glob(["*.h"]),
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:wallet",
        "@boost.chrono",
        "@denarii_external//:liblzma",
        "@denarii_external//:libreadline",
        "@denarii_external//:libsodium",
        "@denarii_external//:libunwind",
    ],
)
