package(default_visibility = ["//visibility:public"])

cc_test(
    name = "cnccrypto_tests",
    srcs = [
        "crypto.cpp",
        "crypto-ops.c",
        "crypto-ops-data.c",
        "crypto-tests.h",
        "hash.c",
        "main.cpp",
        "random.cs",
    ],
    deps = ["//src/common"],
)

cc_test(
    name = "cnv4_jit_tests",
    srcs = ["cnv4-jit.c"],
    deps = ["//src/common"],
)
