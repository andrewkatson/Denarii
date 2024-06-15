package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "block_fuzz_tests",
    srcs = [
        "block.cpp",
        "fuzzer.cpp",
        "fuzzer.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//other:liblzma",
        "//other:libreadline",
        "//other:libsodium",
        "//other:libunwind",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
    ],
)

cc_binary(
    name = "transaction_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "transaction.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//other:liblzma",
        "//other:libreadline",
        "//other:libsodium",
        "//other:libunwind",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
    ],
)

cc_binary(
    name = "signature_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "signature.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lunwind",
        "-lreadline",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:wallet",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "cold_outputs_fuzz_tests",
    srcs = [
        "cold-outputs.cpp",
        "fuzzer.cpp",
        "fuzzer.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:wallet",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "cold_transaction_fuzz_tests",
    srcs = [
        "cold-transaction.cpp",
        "fuzzer.cpp",
        "fuzzer.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_core",
        "//src:device",
        "//src:p2p",
        "//src:wallet",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "load_from_binary_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "load_from_binary.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.program_options",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "load_from_json_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "load_from_json.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.program_options",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "base58_fuzz_tests",
    srcs = [
        "base58.cpp",
        "fuzzer.cpp",
        "fuzzer.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.program_options",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "pares_url_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "parse_url.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.program_options",
        "@boost.regex",
        "@boost.system",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "http_client_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "http-client.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.chrono",
        "@boost.program_options",
        "@boost.regex",
        "@boost.system",
        "@boost.thread",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "levin_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "levin.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost.chrono",
        "@boost.program_options",
        "@boost.regex",
        "@boost.thread",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "bulletproof_fuzz_tests",
    srcs = [
        "bulletproof.cpp",
        "fuzzer.cpp",
        "fuzzer.h",
    ],
    linkopts = [
        "-ltinfo",
        "-lreadline",
        "-lunwind",
        "-llzma",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_basic",
        "@boost.chrono",
        "@boost.program_options",
        "@boost.regex",
        "@boost.thread",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)

cc_binary(
    name = "tx_extra_fuzz_tests",
    srcs = [
        "fuzzer.cpp",
        "fuzzer.h",
        "tx-extra.cpp",
    ],
    linkopts = [
        "-ltinfo",
        "-lunwind",
        "-llzma",
        "-lreadline",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_basic",
        "@boost.chrono",
        "@boost.program_options",
        "@boost.regex",
        "@boost.system",
        "@boost.thread",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@libunwind",
    ],
)
