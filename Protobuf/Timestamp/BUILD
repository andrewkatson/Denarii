load("@rules_cc//cc:defs.bzl", "cc_library", "cc_test")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "timestamp_helpers",
    srcs = ["timestamp_helpers.cc"],
    hdrs = ["timestamp_helpers.h"],
    deps = [
        "//ProtoBuf/Duration/Proto:duration_cc_proto",
        "//ProtoBuf/Timestamp/Proto:timestamp_cc_proto",
        "//Tools/General/Math:bits",
        "@com_google_absl//absl/strings",
        "@com_google_absl//absl/strings:str_format",
        "@com_google_absl//absl/time",
    ],
)

