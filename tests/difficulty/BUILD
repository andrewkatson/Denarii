package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "difficulty",
    srcs = ["difficulty.cpp"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//other:liblzma",
        "//other:libreadline",
        "//src:cryptonote_basic",
    ],
)

py_binary(
    name = "wide_difficulty",
    srcs = ["wide_difficulty.py"],
    deps = [],
)
