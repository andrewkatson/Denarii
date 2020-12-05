package(default_visibility = ["//visibility:public"])

cc_test(
    name = "functional_tests",
    srcs = [
        "main.cpp",
        "transactions_flow_test.cpp",
        "transactions_flow_test.h",
        "transactions_generation_from_blockchain.cpp",
        "transactions_generation_from_blockchain.h",
    ],
    deps = [
        "//contrib/epee",
        "//src/common",
        "//src/crypto:cncrypto",
        "//src/cryptonote_core",
        "//src/wallet",
        "@boost//:program_options",
        "@boost//:regex",
    ],
)

cc_test(
    name = "make_test_signature",
    srcs = ["make_test_signature.cc"],
    deps = [
        "//contrib/epee",
        "//src/crypto:cncrypto",
        "//src/rpc:rpc_base",
    ],
)

py_test(
    name = "check_missing_rpc_methods",
    srcs = [
        "address_book.py",
        "bans.py",
        "blockchain.py",
        "check_missing_rpc_methods.py",
        "cold_signing.py",
        "daemon_info.py",
        "functional_tests_rpc.py",
        "get_output_distribution.py",
        "integrated_address.py",
        "mining.py",
        "multisig.py",
        "p2p.py",
        "proofs.py",
        "rpc_payment.py",
        "sign_message.py",
        "speed.py",
        "transfer.py",
        "txpool.py",
        "uri.py",
        "validate_address.py",
        "wallet.py",
    ],
    deps = [],
)
