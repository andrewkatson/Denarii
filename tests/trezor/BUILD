package(default_visibility = ["//visibility:public"])

cc_test(
    name = "trezor",
    srcs = [
        "daemon.cpp",
        "daemon.h",
        "tools.cpp",
        "tools.h",
        "trezor_tests.cpp",
        "trezor_tests.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "//src/device",
        "//src/device_trezor",
        "//src/multisig",
        "//src/p2p",
        "//src/rpc",
        "//src/rpc:daemon_rpc_server",
        "//src/wallet",
        "//src/wallet/api:wallet_api",
        "@libzmq",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:system",
    ],
)
