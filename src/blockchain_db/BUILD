package(default_visibility = ["//visibility:public"])

cc_library(
    name = "blockchain_db",
    srcs = [
        "blockchain_db.cpp",
        "lmdb/db_lmdb.cpp",
    ],
    hdrs = [
        "blockchain_db.h",
        "lmdb/db_lmdb.h",
    ],
    deps = [
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/ringct",
        "@db_drivers",
        "@rules_boost//:filesystem",
        "@rules_boost//:thread",
    ],
)
