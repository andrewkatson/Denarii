package(default_visibility = ["//visibility:public"])

cc_test(
    name = "block_fuzz_tests",
    srcs = [
        "block.cpp",
        "fuzzer.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
    ],
)

cc_test(
    name = "transaction_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "transaction.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
    ],
)

cc_test(
    name = "signature_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "signature.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
        "//src/wallet",
    ],
)

cc_test(
    name = "cold_outputs_fuzz_tests",
    srcs = [
        "cold-outputs.cpp",
        "fuzzer.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
        "//src/wallet",
    ],
)

cc_test(
    name = "cold_transaction_fuzz_tests",
    srcs = [
        "cold-transaction.cpp",
        "fuzzer.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/cryptonote_core",
        "//src/device",
        "//src/p2p",
        "//src/wallet",
    ],
)

cc_test(
    name = "load_from_binary_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "load_from_binary.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@boost//:program_options",
    ],
)

cc_test(
    name = "load_from_json_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "load_from_json.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@boost//:program_options",
    ],
)

cc_test(
    name = "base58_fuzz_tests",
    srcs = [
        "base58.cpp",
        "fuzzer.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@boost//:program_options",
    ],
)

cc_test(
    name = "pares_url_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "parse_url.cpp",
    ],
    deps = [
        "//contrib/epee",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:system",
    ],
)

cc_test(
    name = "http_client_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "http-client.cpp",
    ],
    deps = [
        "//contrib/epee",
        "@boost//:chrono",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:system",
        "@boost//:thread",
    ],
)

cc_test(
    name = "levin_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "levin.cpp",
    ],
    deps = [
        "//contrib/epee:",
        "//src/common",
        "@boost//:chrono",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:thread",
    ],
)

cc_test(
    name = "bulletproof_fuzz_tests",
    srcs = [
        "bulletproof.cpp",
        "fuzzer.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "@boost//:chrono",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:thread",
    ],
)

cc_test(
    name = "tx_extra_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "tx-extra.cpp",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "//src/cryptonote_basic",
        "@boost//:chrono",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:system",
        "@boost//:thread",
    ],
)
