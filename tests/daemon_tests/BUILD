package(default_visibility = ["//visibility:public"])

cc_test(
    name = "transfers",
    srcs = ["transfers.cpp"],
    deps = [
        "//contrib/epee",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:rpc",
        "//src/wallet/api:wallet_api",
        "@com_google_googletest//:gtest_main",
    ],
)
