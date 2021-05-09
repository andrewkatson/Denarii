package(default_visibility = ["//visibility:public"])


cc_binary(
    name = "lvalue_issue",
    srcs = ["lvalue_issue.cpp"],
    deps = [],
)

cc_binary(
    name = "miscellaneous",
    srcs = ["miscellaneous.cpp"],
    deps = ["//src:blockchain_db"],
    copts = ["-Wa,-mbig-obj"],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ],
)