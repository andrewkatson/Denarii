package(default_visibility = ["//visibility:public"])

cc_test(
    name = "performance_tests",
    srcs = ["main.cpp"] + glob(["*.h"]),
    deps = [
        "//contrib/epee",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/wallet",
        "@rules_boost//:chrono",
    ],
)
