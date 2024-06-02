package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "hash_tests",
    srcs = ["main.cpp"],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//tests:io",
        "@denarii_external//:liblzma",
    ],
)
