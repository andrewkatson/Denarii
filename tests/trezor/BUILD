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
        "//other:libzmq",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:daemon_files_for_test",
        "//src:daemon_rpc_server",
        "//src:device",
        "//src:p2p",
        "//src:rpc",
        "//src:version",
        "//src:wallet",
        "//src/device_trezor",
        "//src/multisig",
        "//src/wallet/api:wallet_api",
        "//tests/core_tests:tools",
        "@boost.chrono",
        "@boost.filesystem",
        "@boost.program_options",
        "@boost.system",
    ],
)
