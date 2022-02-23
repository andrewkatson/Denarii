package(default_visibility = ["//visibility:public"])


cc_binary(
    name = "lvalue_issue",
    srcs = ["lvalue_issue.cpp"],
    deps = [],
)

cc_binary(
    name = "miscellaneous",
    srcs = ["miscellaneous.cpp",         "blockchain_utilities/blockchain_export.cpp",
                                         "blockchain_utilities/blockchain_utilities.h",
                                         "blockchain_utilities/blocksdat_file.cpp",
                                         "blockchain_utilities/blocksdat_file.h",
                                         "blockchain_utilities/bootstrap_file.cpp",
                                         "blockchain_utilities/bootstrap_file.h",
                                         "blockchain_utilities/bootstrap_serialization.h",
                                         "serialization/difficulty_type.h",
                                         "serialization/json_utils.h",],
    deps = ["//src:blockchain_db"],
    copts = ["-Wa,-mbig-obj"],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ],
)

cc_binary(
    name = "asio_stuff",
    srcs = [":asio_stuff.cpp"],
    deps = [
        "//contrib/epee:epee",
                "@boost//:asio_ssl",
                "@boost//:chrono",
                "@boost//:filesystem",
                "@boost//:program_options",
                "@boost//:thread",
                "@liblzma",],
            linkopts = [
                "-lssl",
                "-lcrypto",
                "-lws2_32",
                "-lwsock32",
            ]
)

cc_library(
    name = "include_this",
    srcs = ["include_this.cpp"],
    hdrs = ["include_this.h"],
    deps = ["@randomx//:randomx_lib",],
)

cc_binary(
    name = "randomx_stuff",
    srcs = ["randomx_stuff.cpp", "randomx_stuff.h"],
    linkopts = [
        "-lssl",
        "-lcrypto",
        "-lbcrypt",
        "-lws2_32",
        "-lwsock32",
        "-lpthread",
        "-L external/randomx/build", "-lrandomx"
    ],
    deps = [
        "//src:wallet",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:rpc_base",
        "//src:version",
        "//src/daemonizer",
        "@boost//:asio_ssl",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:thread",
        "@liblzma",
    ],
)