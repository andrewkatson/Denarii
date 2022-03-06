package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "denarii_gen_ssl_cert",
    srcs = ["gen_ssl_cert.cpp"],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@liblzma",
    ],
)
