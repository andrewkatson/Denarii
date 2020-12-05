package(default_visibility = ["//visibility:public"])

cc_test(
    name = "unit_tests",
    srcs = glob([
        "*.h",
        "*.cpp",
    ]),
    copts = [
        "--data-dir",
        "../data",
    ],
    deps = [
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "//src/lmdb",
        "//src/net",
        "//src/p2p",
        "//src/ringct",
        "//src/rpc",
        "//src/rpc:daemon_messages",
        "//src/rpc:daemon_rpc_server",
        "//src/serialization",
        "//src/wallet",
        "@boost//:chrono",
        "@boost//:thread",
        "@gtest",
        "@libzmq",
    ],
)

cc_test(
    name = "test_notifier",
    srcs = ["test_notifier.cpp"],
    deps = [],
)
