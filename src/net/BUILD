package(default_visibility = ["//visibility:public"])

cc_library(
    name = "net",
    srcs = [
        "dandelionpp.cpp",
        "error.cpp",
        "http.cpp",
        "i2p_address.cpp",
        "parse.cpp",
        "socks.cpp",
        "socks_connect.cpp",
        "tor_address.cpp",
        "zmq.cpp",
    ],
    hdrs = [
        "dandelionpp.h",
        "error.h",
        "http.cpp",
        "i2p_address.h",
        "parse.h",
        "socks.h",
        "socks_connect.h",
        "tor_address.h",
        "zmq.h",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@boost_rules//:asio",
        "@libzmq",
    ],
)
