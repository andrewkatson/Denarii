package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "test",
    srcs = ["test.cc"],
    deps = [
        "@boost",
        "@db_drivers",
        "@easy_logging",
        "@expat",
        "@ldns",
        "@libhidapi",
        "@liblzma",
        "@libnorm",
        "@libreadline",
        "@libsodium",
        "@libudev",
        "@libunbound",
        "@libunwind",
        "@libusb",
        "@libzmq",
        "@lrelease",
        "@miniupnp//:minissdpd",
        "@miniupnp//:miniupnpc",
        "@miniupnp//:miniupnpc-async",
        "@miniupnp//:miniupnpc-libevent",
        "@miniupnp//:miniupnpc-libuv",
        "@miniupnp//:miniupnpd",
        "@openpgm",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
        "@qrcodegen",
        "@randomx",
        "@rapidjson",
        "@supercop",
        "@trezor_common//protob:messages_cc_proto",
        "@trezor_common//protob:messages_common_cc_proto",
        "@trezor_common//protob:messages_management_cc_proto",
        "@trezor_common//protob:messages_monero_cc_proto",
        "@unbound",
    ],
)

py_binary(
    name = "configure",
    srcs = ["configure.py"],
    deps = [],
)

py_binary(
    name = "configure_win",
    srcs = ["configure_win.py"],
    deps = [],
)