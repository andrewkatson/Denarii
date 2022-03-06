package(default_visibility = ["//visibility:public"])

cc_library(
    name = "blocks",
    srcs = [
        "blocks.cpp",
        "generated_checkpoints.c",
        "generated_stagenet_blocks.c",
        "generated_testnet_blocks.c",
    ],
    hdrs = ["blocks.h"],
    deps = [
        "//contrib/epee",
        "//src:config",
    ],
)
