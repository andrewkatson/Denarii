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
    ], exclude = ["src/readline_buffer.cpp"]),
    hdrs = glob([
        "**/*.h",
        "**/*.hpp",
        "**/*.inl",
    ]),
    linkopts = select({
        "windows": ["-lssl","-lcrypto","-lcrypt32", "-lws2_32","-lwsock32"],
        "mac": [],
        "//conditions:default": ["-lssl","-lcrypto",],
    }),
    deps = [
        "@boost//:assign",
        "@boost//:chrono",
        "@boost//:asio_ssl",
        "@boost//:filesystem",
        "@boost//:thread",
        "@boost//:multiprecision",
        "@boost//:interprocess",
        "@boost//:mpl",
        "@boost//:uuid",
        "@easy_logging",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
        "@openssl//:ssl",
        "@libreadline//:libreadline",
        "@zlib",
    ],
)
