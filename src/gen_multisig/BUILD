package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_gen_trusted_multisig",
    srcs = ["gen_multisig.cpp"],
    deps = [
        "//contrib/epee",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:wallet",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:thread",
        "@liblzma",
        "@libreadline",
    ],
)
