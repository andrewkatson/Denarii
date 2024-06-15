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
        "//other:liblzma",
        "//other:libreadline",
        "//other:libsodium",
        "//other:libunwind",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:wallet",
        "@boost.chrono",
    ],
)
