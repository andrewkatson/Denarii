package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_utils_deserialize",
    srcs = ["cn_deserialize.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:ringct",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_utils_object_sizs",
    srcs = ["object_sizes.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:p2p",
        "//src/wallet/api:wallet_api",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_utils_dns_checks",
    srcs = ["dns_checks.cpp"],
    deps = [
        "//src:common",
        "//src:version",
        "@boost.program_options",
        "@boost.system",
        "@liblzma",
    ],
)
