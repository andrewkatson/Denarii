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

config_setting(
    name = "linux",
    constraint_values = [
        "@platforms//os:linux",
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "epee",
    srcs = glob(
        [
            "src/*.cpp",
            "src/*.c",
        ],
        exclude = ["src/readline_buffer.cpp"],
    ),
    hdrs = glob([
        "**/*.h",
        "**/*.hpp",
        "**/*.inl",
    ]),
    linkopts = [
        "-Lother/openssl",
        "-lssl",
        "-lcrypto",
    ] + select({
        "windows": [
            "-lcrypt32",
            "-lws2_32",
            "-lwsock32",
        ],
        "mac": [],
        "linux": [],
    }),
    deps = [
        "//other:libreadline",
        "//other:spdlog",
        "@boost.asio",
        "@boost.assign",
        "@boost.chrono",
        "@boost.filesystem",
        "@boost.foreach",
        "@boost.interprocess",
        "@boost.lambda",
        "@boost.mpl",
        "@boost.multiprecision",
        "@boost.spirit",
        "@boost.thread",
        "@boost.timer",
        "@boost.uuid",
        "@openssl:crypto",
        "@openssl:ssl",
        "@zlib",
    ],
)
