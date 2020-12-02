package(default_visibility = ["//visibility:public"])

cc_library(
    name = "wallet",
    srcs = [
        "message_store.cpp",
        "message_transporter.cpp",
        "node_rpc_proxy.cpp",
        "ringdb.cpp",
        "wallet2.cpp",
        "wallet_args.cpp",
        "wallet_rpc_payments.cpp",
    ],
    hdrs = [
        "message_store.h",
        "message_transporter.h",
        "node_rpc_proxy.h",
        "ringdb.h",
        "wallet2.h",
        "wallet_args.h",
        "wallet_errors.h",
        "wallet_rpc_helpers.h",
        "wallet_rpc_server.h",
        "wallet_rpc_server_commands_defs.h",
        "wallet_rpc_server_error_codes.h",
    ],
    deps = [
        "//src/common",
        "//src/cryptonote_core",
        "//src/device_trezor",
        "//src/mnemonics",
        "//src/multisig",
        "//src/net",
        "//src/rpc:rpc_base",
        "@db_drivers",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:regex",
        "@rules_boost//:serialization",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)

cc_binary(
    name = "denarii_wallet_rpc_server",
    srcs = [
        "wallet_rpc_server.cpp",
        "wallet_rpc_server.h",
    ],
    deps = [
        ":wallet",
        "//src:version",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/daemonizer",
        "//src/rpc:rpc_base",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:thread",
    ],
)
