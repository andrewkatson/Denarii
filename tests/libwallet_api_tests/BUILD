cc_test(
    name = "libwallet_api_tests",
    srcs = ["main.cpp"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//contrib/epee",
        "//src:device",
        "//src:version",
        "//src/wallet/api:wallet_api",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:locale",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
        "@gtest",
        "@liblzma",
        "@libreadline",
    ],
)
