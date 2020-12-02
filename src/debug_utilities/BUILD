package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_utils_deserialize",
    srcs = ["cn_deserialize.cpp"],
    deps = [
        "//contrib/epee",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
        "//src/ringct",
    ],
)

cc_binary(
    name = "denarii_utils_object_sizs",
    srcs = ["object_sizes.cpp"],
    deps = [
        "//contrib/epee",
        "//src/blockchain_db",
        "//src/cryptonote_core",
        "//src/p2p",
    ],
)

cc_binary(
    name = "denarii_utils_dns_checks",
    srcs = ["dns_checks.cpp"],
    deps = [
        "//src:version",
        "//src/common",
        "@rules_boost//:program_options",
        "@rules_boost//:system",
    ],
)
