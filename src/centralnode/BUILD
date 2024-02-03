package(default_visibility = ["//visibility:public"])

cc_library(
    name = "dynamic_critical_values",
    srcs = ["dynamic_critical_values.cpp"],
    hdrs = ["dynamic_critical_values.h"],
    data = [":critical_values_textpb"],
    deps = [
        "//src/centralnode/Proto:critical_values_cc_proto",
        "//ProtoBuf/TextProto:read_text_proto",
    ],
)

filegroup(
    name = "critical_values_textpb",
    srcs = ["critical_values.textpb"],
)
