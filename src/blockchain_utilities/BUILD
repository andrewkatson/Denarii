package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_blockchain_export",
    srcs = [
        "blockchain_export.cpp",
        "blocksdat_file.cpp",
        "blocksdat_file.h",
        "bootstrap_file.cpp",
        "bootstrap_file.h",
        "bootstrap_serialization.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:system",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_import",
    srcs = [
        "blockchain_import.cpp",
        "blocksdat_file.cpp",
        "blocksdat_file.h",
        "bootstrap_file.cpp",
        "bootstrap_file.h",
        "bootstrap_serialization.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/blocks",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_blackball",
    srcs = [
        "blockchain_blackball.cpp",
        "blocksdat_file.h",
        "bootstrap_file.h",
        "bootstrap_serialization.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/wallet",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_usage",
    srcs = ["blockchain_usage.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_ancestry",
    srcs = ["blockchain_ancestry.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_prune_know_spent_data",
    srcs = ["blockchain_prune_known_spent_data.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/p2p",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_prune",
    srcs = ["blockchain_prune.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/p2p",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_depth",
    srcs = ["blockchain_depth.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)

cc_binary(
    name = "denarii_blockchain_stats",
    srcs = ["blockchain_stats.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "@boost_rules//:filesystem",
        "@boost_rules//:thread",
    ],
)
