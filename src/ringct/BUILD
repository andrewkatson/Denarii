package(default_visibility = ["//visibility:public"])

cc_library(
    name = "ringct_basic",
    srcs = [
        "bulletproofs.cc",
        "multiexp.cc",
        "rctCryptoOps.c",
        "rctOps.cpp",
        "rctTypes.cpp",
    ],
    hdrs = [
        "bulletproofs.h",
        "multiexp.h",
        "rctOps.h",
        "rctTypes.h",
    ],
    deps = [
        "//src/common",
        "//src/crypto:cncrypto",
        "@openssl",
    ],
)

cc_library(
    name = "ringct",
    srcs = ["rctSigs.cpp"],
    hdrs = ["rctSigs.h"],
    deps = [
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_basic",
        "//src/device",
        "@openssl",
    ],
)
