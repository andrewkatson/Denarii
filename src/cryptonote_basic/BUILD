package(default_visibility = ["//visibility:public"])

cc_library(
    name = "cryptonote_basic",
    srcs = [
        "account.cpp",
        "cryptonote_basic_impl.cpp",
        "cryptonote_format_utils.cpp",
        "difficulty.cpp",
        "hardfork.cpp",
        "miner.cpp",
    ],
    hdrs = [
        "account.h",
        "account_boost_serialization.h",
        "connection_context.h",
        "cryptonote_basic.h",
        "cryptonote_basic_impl.h",
        "cryptonote_boost_serialization.h",
        "cryptonote_format_utils.h",
        "difficulty.h",
        "hardfork.h",
        "miner.h",
        "tx_extra.h",
        "verification_context.h",
    ],
    deps = [
        "//src/checkpoints",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/device",
        "@rules_boost//:date_time",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:serialization",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)
