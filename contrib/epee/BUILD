package(default_visibility = ["//visibility:public"])

cc_library(
    name = "epee",
    srcs = glob([
        "src/*.cpp",
        "src/*.c",
    ]),
    hdrs = glob([
        "**/*.h",
        "**/*.hpp",
        "**/*.inl",
    ]),
    linkopts = [
        "-lssl",
        "-lcrypto",
        "-lws2_32",
        "-lwsock32",
        "-lcrypt32",
    ],
    deps = [
        "@boost//:chrono",
        "@boost//:asio_ssl",
        "@boost//:filesystem",
        "@boost//:thread",
        "@easy_logging",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
        "@libreadline//:libreadline",
        "@zlib",
    ],
)
