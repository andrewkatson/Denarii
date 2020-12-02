package(default_visibility = ["//visibility:public"])

cc_library(
    name = "serialization",
    srcs = ["json_object.cpp"],
    hdrs = ["json_object.h"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/cryptonote_basic",
        "//src/cryptonote_core",
        "//src/cryptonote_protocol",
        "@rules_boost//:chrono",
        "@rules_boost//:regex",
        "@rules_boost//:system",
        "@rules_boost//:thread",
    ],
)
