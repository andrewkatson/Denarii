package(default_visibility = ["//visibility:public"])

cc_library(
    name = "p2p",
    srcs = [
        "net_node.cpp",
        "net_peerlist.cpp",
    ],
    hdrs = [
        "net_node.h",
        "net_node.inl",
        "net_node_common.h",
        "net_peerlist.cpp",
        "net_peerlist_boost_serialization.h",
        "p2p_protocol_defs.h",
        "stdafx.h",
    ],
    deps = [
        "//src:version",
        "//src/cryptonote_core",
        "//src/net",
        "@miniupnp//:miniupnpc",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:serialization",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)
