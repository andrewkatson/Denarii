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
    deps = [
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:thread",
        "@easy_logging",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
        "@libreadline//:libreadline",
        "@zlib",
    ],
)
