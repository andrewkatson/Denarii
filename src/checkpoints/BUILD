package(default_visibility = ["//visibility:public"])

cc_library(
    name = "checkpoints",
    srcs = ["checkpoints.cpp"],
    hdrs = ["checkpoints.h"],
    deps = [
        "//src/common",
        "//src/crypto:cncrypto",
        "@rules_boost//:date_time",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
        "@rules_boost//:serialization",
        "@rules_boost//:system",
        "@rules_boost//:thread,",
    ],
)
