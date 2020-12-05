package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_wallet_cli",
    srcs = [
        "simplewallet.cpp",
        "simplewallet.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:rpc_base",
        "//src:version",
        "//src:wallet",
        "//src/mnemonics",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:locale",
        "@boost//:program_options",
        "@boost//:thread",
        "@liblzma",
        "@libreadline",
        "@qrcodegen",
    ],
)
