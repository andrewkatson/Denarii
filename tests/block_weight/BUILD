cc_binary(
    name = "block_weight",
    srcs = ["block_weight.cpp"],
    linkopts = [
        "-ltinfo",
        "-lreadline",
    ],
    deps = [
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "@liblzma",
        "@libreadline",
    ],
)

py_binary(
    name = "block_weight_py",
    srcs = [
        "block_weight.py",
    ],
    main = "block_weight.py",
    deps = [],
)

py_binary(
    name = "compare",
    srcs = ["compare.py"],
    deps = [],
)
