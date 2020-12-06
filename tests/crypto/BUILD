package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "cnccrypto_tests",
    srcs = [
        "crypto.cpp",
        "crypto-ops.c",
        "crypto-tests.h",
        "hash.c",
        "main.cpp",
        "random.c",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//src:cnccrypto_for_tests",
        "//src:cncrypto",
        "//src:common",
        "//tests:io",
        "@liblzma",
        "@libreadline",
    ],
)

cc_binary(
    name = "cnv4_jit_tests",
    srcs = ["cnv4-jit.c"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "@liblzma",
        "@libreadline",
    ],
)
