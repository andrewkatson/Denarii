package(default_visibility = ["//visibility:public"])

config_setting(
    name = "windows",
    constraint_values = [
        "@bazel_tools//platforms:windows",
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "dynamic_critical_values",
    srcs = ["dynamic_critical_values.cpp"],
    hdrs = ["dynamic_critical_values.h"],
    deps = [
        "//src:net",
        "//src/protobuf:asio_adapting",
        "//src/protobuf:protobuf_helpers",
        "@boost//:thread",
        "@keiros_public//Reactor/CriticalValuesCalculator/Proto:critical_values_calculation_cc_proto",
        "@keiros_public//Reactor/Proto:critical_values_info_request_cc_proto",
        "@keiros_public//Reactor/Proto:critical_values_info_response_cc_proto",
        "@keiros_public//Reactor/Proto/Event/Base:event_cc_proto",
    ] + select({
                     "windows": [],
                     "//conditions:default": ["@boost//:asio",],
                 }),
)
