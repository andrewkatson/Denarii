package(default_visibility = ["//visibility:public"])

cc_test(
    name = "difficulty",
    srcs = ["difficulty.cpp"],
    deps = ["//src/cryptonote_basic"],
)

py_test(
    name = "wide_difficulty",
    srcs = [
        "gen_wide_data.py",
        "generate-data",
        "wide_difficulty.py",
    ],
    deps = [],
)
