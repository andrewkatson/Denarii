package(default_visibility = ["//visibility:public"])

cc_library(
    name = "rpc_base",
    srcs = [
        "rpc_args.cpp",
        "rpc_handler.cpp",
        "rpc_payment_signature.cpp",
    ],
    hdrs = [
        "rpc_args.h",
        "rpc_handler.h",
        "rpc_payment_signature.h",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@rules_boost//:program_options",
        "@rules_boost//:regex",
        "@rules_boost//:thread",
    ],
)

cc_library(
    name = "rpc",
    srcs = [
        "bootstrap_daemon.cpp",
        "bootstrap_node_selector.cpp",
        "core_rpc_server.cpp",
        "instanciations.cpp",
        "rpc_payment.cpp",
        "rpc_version_str.cpp",
    ],
    hdrs = [
        "rpc_handler.h",
        "rpc_version_str.h",
    ],
    deps = [
        ":rpc_base",
        "//src:version",
        "//src/common",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "//src/net",
        "@rules_boost//:regex",
        "@rules_boost//:thread",
    ],
)

cc_library(
    name = "rpc_pub",
    srcs = ["zmq_pub.cpp"],
    hdrs = ["zmq_pub.h"],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_basic",
        "//src/net",
        "//src/serialization",
        "@rules_boost//:thread",
    ],
)

cc_library(
    name = "daemon_messages",
    srcs = [
        "daemon_messages.cpp",
        "message.cpp",
    ],
    hdrs = [
        "daemon_messages.h",
        "message.h",
    ],
    deps = [
        "//src:version",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "//src/serialization",
    ],
)

cc_library(
    name = "daemon_rpc_server",
    srcs = [
        "daemon_handler.cpp",
        "zmq_pub.cpp",
        "zmq_server.cpp",
    ],
    hdrs = [
        "daemon_handler.h",
        "daemon_messages.h",
        "message.h",
        "zmq_server.h",
    ],
    deps = [
        ":daemon_messages",
        ":rpc",
        ":rpc_pub",
        "//src:version",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "//src/serialization",
        "@libzmq",
        "@rules_boost//:chrono",
        "@rules_boost//:regex",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)
