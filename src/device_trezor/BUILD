package(default_visibility = ["//visibility:public"])

config_setting(
    name = "windows",
    constraint_values = [
        "@platforms//os:windows",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "mac",
    constraint_values = [
        "@platforms//os:macos",
    ],
    visibility = ["//visibility:public"],
)

cc_library(
    name = "device_trezor",
    srcs = [
        "device_trezor.cpp",
        "device_trezor_base.cpp",
        "trezor/messages_map.cpp",
        "trezor/protocol.cpp",
        "trezor/transport.cpp",
    ],
    hdrs = [
        "device_trezor.hpp",
        "device_trezor_base.hpp",
        "trezor.hpp",
        "trezor/exceptions.hpp",
        "trezor/messages_map.hpp",
        "trezor/protocol.hpp",
        "trezor/transport.hpp",
        "trezor/trezor_defs.hpp",
    ] + select({
        "windows": glob(["**/trezor/include/*.h"]),
        "mac": [],
        "//conditions:default": [],
    }),
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:ringct_basic",
        "//src:rpc",
        "@boost//:chrono",
        "@libsodium",
        "@libusb",
        "@rapidjson",
        "@trezor_common//protob:messages_cc_proto",
        "@trezor_common//protob:messages_common_cc_proto",
        "@trezor_common//protob:messages_management_cc_proto",
        "@trezor_common//protob:messages_monero_cc_proto",
    ],
)

# unclear if this is ever needed
cc_library(
    name = "minimal_device_trezor",
    srcs = [
        "device_trezor.cpp",
        "trezor.hpp",
        "trezor/trezor_defs.hpp",
    ],
    hdrs = ["device_trezor.hpp"],
    deps = ["//src:device"],
)
