package(default_visibility = ["//visibility:public"])

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
    ],
    deps = [
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/device",
        "//src/ringct:ringct_basic",
        "@libsodium",
        "@libusb",
        "@rules_boost//:chrono",
        "@trezor_common//protob:messages_cc_proto",
        "@trezor_common//protob:messages_common_cc_proto",
        "@trezor_common//protob:messages_management_cc_proto",
        "@trezor_common//protob:messages_monero_cc_proto",
    ],
)

# unclear if this is ever needed
cc_library(
    name = "minimal_device_trezor",
    srcs = ["device_trezor.cpp"],
    hdrs = ["device_trezor.hpp"],
    deps = [],
)
