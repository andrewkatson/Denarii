package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_gen_trusted_multisig",
    srcs = ["gen_multisig.cpp"],
    deps = [
        "//contrib/epee",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/wallet",
        "@libreadline",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:thread",
    ],
)
