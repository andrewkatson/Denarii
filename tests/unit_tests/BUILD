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
        "//src/centralnode:dynamic_critical_values",
        "//src/checkpoints:checkpoints_for_tests",
        "//src/lmdb",
        "//src/protobuf:asio_adapting",
        "//src/protobuf:protobuf_helpers",
        "//src/simplewallet:denarii_wallet_cli",
        "//src/wallet/api:wallet_api",
        "//tests:io",
        "@boost//:chrono",
        "@boost//:thread",
        "@gtest",
        "@keiros_public//Reactor/CriticalValuesCalculator/Proto:critical_values_calculation_cc_proto",
        "@keiros_public//Reactor/Proto:critical_values_info_request_cc_proto",
        "@keiros_public//Reactor/Proto:critical_values_info_response_cc_proto",
        "@keiros_public//Reactor/Proto/Event/Base:event_cc_proto",
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
