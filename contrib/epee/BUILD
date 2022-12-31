package(default_visibility = ["//visibility:public"])

config_setting(
    name = "windows",
    constraint_values = [
        "@platforms//os:windows",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "mac",
    constraint_values = [
        "@platforms//os:macos",
    ],
    visibility = ["//visibility:public"],
)

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
    ]   + select({
        "windows": ["-lcrypt32", "-lws2_32","-lwsock32"],
        "mac": [],
        "//conditions:default": [],
    }),
    deps = [
        "@boost//:assign",
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
