package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "difficulty",
    srcs = ["difficulty.cpp"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//src:cryptonote_basic",
        "@denarii_external//:liblzma",
        "@denarii_external//:libreadline",
    ],
)

py_binary(
    name = "wide_difficulty",
    srcs = ["wide_difficulty.py"],
    deps = [],
)
