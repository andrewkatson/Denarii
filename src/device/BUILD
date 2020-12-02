package(default_visibility = ["//visibility:public"])

cc_library(
    name = "device",
    srcs = [
        "device.cpp",
        "device_default.cpp",
        "device_io_hid.cpp",
        "device_ledger.cpp",
        "log.cpp",
    ],
    hdrs = [
        "device.hpp",
        "device_cold.hpp",
        "device_default.hpp",
        "device_io.hpp",
        "device_io_hid.hpp",
        "device_ledger.hpp",
        "log.hpp",
    ],
    deps = [
        "//src:version",
        "//src/blocks",
        "//src/crypto:cncrypto",
        "//src/crypto/wallet:wallet-crypto",
        "//src/ringct:ringct_basic",
        "@hidapi",
        "@openssl",
        "@rules_boost//:serialization",
    ],
)
