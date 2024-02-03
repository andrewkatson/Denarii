package(default_visibility = ["//visibility:public"])

cc_test(
    name = "unit_tests",
    srcs = glob(
        [
            "*.h",
            "*.cpp",
        ],
        exclude = ["test_notifier.cpp"],
    ),
    copts = [
        "-DDEFAULT_DATA_DIR=\\\"/home/andrew/denarii/tests/data\\\"",
        "-Wno-undef",
        "-Wno-sign-compare",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
        "-lzmq",
        "-lsodium",
    ],
    deps = [
        "//src:blockchain_db",
        "//src:common",
        "//src:common_for_tests",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:daemon_messages",
        "//src:daemon_rpc_server",
        "//src:net",
        "//src:p2p",
        "//src:ringct",
        "//src:rpc",
        "//src:serialization",
        "//src:version",
        "//src:wallet",
        "//src/checkpoints:checkpoints_for_tests",
        "//src/lmdb",
        "//src/simplewallet:denarii_wallet_cli",
        "//src/wallet/api:wallet_api",
        "//tests:io",
        "@boost//:chrono",
        "@boost//:thread",
        "@com_google_absl//absl/random",
        "@com_google_googletest//:gtest_main",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
        "@libzmq",
    ],
)

cc_binary(
    name = "test_notifier",
    srcs = ["test_notifier.cpp"],
    deps = [],
)

cc_library(
    name = "unit_test_utils",
    srcs = [],
    hdrs = ["unit_tests_utils.h"],
    deps = [],
)
