package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_gen_ssl_cert",
    srcs = ["gen_ssl_cert.cpp"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/common",
        "@rules_boost//:filesystem",
        "@rules_boost//:program_options",
    ],
)
