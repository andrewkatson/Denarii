package(default_visibility = ["//visibility:public"])

cc_library(
    name = "checkpoints",
    srcs = ["checkpoints.cpp"],
    hdrs = ["checkpoints.h"],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_basic",
        "@boost//:date_time",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
    ],
)
