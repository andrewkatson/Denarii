package(default_visibility = ["//visibility:public"])

cc_library(
    name = "cryptonote_core",
    srcs = [
        "blockchain.cpp",
        "cryptonote_core.cpp",
        "cryptonote_tx_utils.cpp",
        "tx_pool.cpp",
        "tx_sanity_check.cpp",
    ],
    hdrs = [
        "blockchain.h",
        "blockchain_storage_boost_serialization.h",
        "cryptonote_core.h",
        "cryptonote_tx_utils.h",
        "tx_pool.h",
        "tx_sanity_check.h",
    ],
    deps = [
        "//src:version",
        "//src/blockchain_db",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/device",
        "//src/hardforks",
        "//src/multisig",
        "//src/ringct",
        "@rules_boost//:date_time",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:serialization",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)
