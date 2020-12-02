package(default_visibility = ["//visibility:public"])

cc_library(
    name = "lmdb",
    srcs = [
        "database.cpp",
        "error.cpp",
        "table.cpp",
        "value_stream.cpp",
    ],
    hdrs = [
        "database.h",
        "error.h",
        "key_stream.h",
        "table.h",
        "transaction.h",
        "util.h",
        "value_stream.h",
    ],
    deps = [
        "//src/common",
        "@db_drivers",
    ],
)
