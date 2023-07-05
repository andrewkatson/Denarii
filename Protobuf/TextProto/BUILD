load("@rules_cc//cc:defs.bzl", "cc_proto_library")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "read_text_proto",
    hdrs = ["read_text_proto.h"],
    deps = [
        "@com_google_protobuf//:protobuf",
        "@com_google_protobuf//:protobuf_headers",
        "@gtest",
    ],
)

cc_library(
    name = "write_text_proto",
    hdrs = ["write_text_proto.h"],
    deps = [
        "@com_google_protobuf//:protobuf",
        "@com_google_protobuf//:protobuf_headers",
        "@gtest",
    ],
)

