package(default_visibility = ["//visibility:public"])

cc_library(
    name = "epee",
    srcs = glob(["src/*.cpp"]),
    hdrs = glob(["**/*.h"]),
    deps = [
        "@easy_logging",
        "@openssl",
        "@rules_boost//:chrono",
        "@rules_boost//:filesystem",
        "@rules_boost//:thread",
    ],
)
