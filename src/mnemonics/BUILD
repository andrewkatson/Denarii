package(default_visibility = ["//visibility:public"])

cc_library(
    name = "mnemonics",
    srcs = ["electrum-words.cpp"],
    hdrs = glob(["*.h"]),
    deps = [
        "//contrib/epee",
        "//src:cncrypto",
        "//src:common",
        "@boost//:system",
        "@easy_logging",
    ],
)
