package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_wallet_cli",
    srcs = [
        "simplewallet.cpp",
        "simplewallet.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/mnemonics",
        "//src/rpc:rpc_base",
        "//src/wallet",
        "@libreadline",
        "@qrcodegen",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:locale",
        "@rules_boost//:program_options",
        "@rules_boost//:thread",
    ],
)
