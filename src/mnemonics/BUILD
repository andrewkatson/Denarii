package(default_visibility = ["//visibility:public"])

cc_library(
    name = "mnemonics",
    srcs = ["electrum-words.cpp"],
    hdrs = glob(["*.h"]),
    deps = [
        "//contrib/epee",
        "@easy_logging",
        "@rules_boost//:system",
    ],
)
