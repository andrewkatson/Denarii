package(default_visibility = ["//visibility:public"])

cc_test(
    name = "net_load_tests_clt",
    srcs = [
        "clt.cpp",
        "net_load_tests.h",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/p2p",
        "@boost//:chrono",
        "@boost//:date_time",
        "@boost//:system",
        "@boost//:thread",
        "@gtest",
    ],
)

cc_test(
    name = "net_load_tests_srv",
    srcs = [
        "net_load_tests.h",
        "srv.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/p2p",
        "@boost//:chrono",
        "@boost//:date_time",
        "@boost//:system",
        "@gtest",
    ],
)
