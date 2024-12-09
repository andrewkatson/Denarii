package(default_visibility = ["//visibility:public"])

config_setting(
    name = "windows",
    constraint_values = [
        "@platforms//os:windows",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "mac",
    constraint_values = [
        "@platforms//os:macos",
    ],
    visibility = ["//visibility:public"],
)

cc_binary(
    name = "denarii_wallet_cli",
    srcs = [
        "simplewallet.cpp",
        "simplewallet.h",
    ],
    linkopts = [
        "-Lexternal/openssl",
        "-lssl",
        "-lcrypto",
        "-ldl",
        "-lpthread",
        "-lboost_system",
        "-lboost_thread",
    ] + select({
        "windows": [],
        "mac": [],
        "//conditions:default": [],
    }),
    deps = [
        "//contrib/epee",
        "//other:liblzma",
        "//other:libreadline",
        "//other:qrcodegen",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:rpc_base",
        "//src:version",
        "//src:wallet",
        "//src/mnemonics",
        "@boost.asio",
        "@boost.chrono",
        "@boost.filesystem",
        "@boost.locale",
        "@boost.program_options",
        "@boost.system",
        "@boost.thread",
        "@openssl:crypto",
        "@openssl:ssl",
    ],
)
