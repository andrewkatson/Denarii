package(default_visibility = ["//visibility:public"])

constraint_setting(name = "cpu")

constraint_value(
    name = "i386",
    constraint_setting = ":cpu",
)

constraint_value(
    name = "amd64",
    constraint_setting = ":cpu",
)

config_setting(
    name = "amd64_config",
    constraint_values = [
        ":amd64",
    ],
    visibility = ["//visibility:public"],
)


config_setting(
    name = "i386_config",
    constraint_values = [
        ":i386",
    ],
    visibility = ["//visibility:public"],
)


config_setting(
    name = "x86_64",
    constraint_values = [
        "@bazel_tools//platforms:x86_64",
    ],
    visibility = ["//visibility:public"],
)

config_setting(
    name = "windows",
    constraint_values = [
        "@bazel_tools//platforms:windows",
    ],
    visibility = ["//visibility:public"],
)

cc_binary(
    name = "denariid",
    srcs = glob(
        [
            "**/cryptonote_protocol/cryptonote_protocol*",
            "**/daemon/*",
            "**/p2p/*",
        ],
        exclude = ["**/*.txt"],
    ) + [
        "rpc/core_rpc_server_commands_defs.h",
        "rpc/rpc_payment_costs.h",
        "serialization/pair.h",
        "wallet/message_store.cpp",
        "wallet/message_transporter.cpp",
        "wallet/node_rpc_proxy.cpp",
        "wallet/ringdb.cpp",
        "wallet/wallet2.cpp",
        "wallet/wallet_args.cpp",
        "wallet/wallet_rpc_payments.cpp",
        "wallet/message_store.h",
        "wallet/message_transporter.h",
        "wallet/node_rpc_proxy.h",
        "wallet/ringdb.h",
        "wallet/wallet2.h",
        "wallet/wallet_args.h",
        "wallet/wallet_errors.h",
        "wallet/wallet_rpc_helpers.h",
        "wallet/wallet_rpc_server_commands_defs.h",
        "wallet/wallet_rpc_server_error_codes.h",
    ],
    linkopts = [
        "-lunwind",
        "-lssl",
        "-lcrypto",
        "-lcrypt",
        "-ldl",
        "-lpthread",
        "-lboost_system",
        "-lboost_thread",
    ],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:daemon_rpc_server",
        "//src:net",
        "//src:p2p",
        "//src:rpc",
        "//src:rpc_base",
        "//src:serialization",
        "//src:version",
        "//src/blocks",
        "//src/centralnode:dynamic_critical_values",
        "//src/daemonizer",
        "//src/device_trezor",
        "//src/mnemonics",
        "//src:multisig",
        "@boost//:asio_ssl",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
        "@db_drivers",
        "@liblzma",
        "@libreadline",
        "@libsodium",
        "@miniupnp//:miniupnpc",
        "@unbound",
        "@libunwind//:libunwind",
    ],
)

cc_library(
    name = "version",
    srcs = ["version.cpp"],
    hdrs = ["version.h"],
    deps = [],
)

cc_library(
    name = "config",
    srcs = [],
    hdrs = ["cryptonote_config.h"],
    deps = [],
)

cc_library(
    name = "cncrypto",
    srcs = glob([
        "**/crypto/*.c",
        "**/crypto/*.cpp",
        "**/crypto/*.S",
    ]) +
    select({
            "windows": glob(["**/crypto/wallet/*.c", "**/crypto/wallet/*.cpp"]),
        }),
    hdrs = glob([
        "**/crypto/*.h",
        "**/varint.h",
        "**/pod-class.h",
    ]) +
          select({
                  "windows": glob(["**/crypto/wallet/*.h"]),
              }),
    copts = [
        "-msse4.1",
        "-maes",
        "-march=native",
    ],
    deps = [
        ":config",
        "//contrib/epee",
        "@boost//:system",
        "@libsodium",
        "@randomx",
    ],
)

# ONLY USE IN TESTS THIS IS A WORKAROUND BECAUSE CMAKE IS WEIRD
cc_library(
    name = "cnccrypto_for_tests",
    srcs = [],
    hdrs = [
        "crypto/crypto.cpp",
        "crypto/crypto-ops.c",
        "crypto/hash.c",
        "crypto/keccak.c",
        "crypto/random.c",
    ],
    copts = [
        "-msse4.1",
        "-maes",
        "-march=native",
    ],
    deps = [
        ":config",
        "//contrib/epee",
        "@boost//:system",
        "@libsodium",
        "@randomx",
    ],
)

cc_library(
    name = "common",
    srcs = glob([
        "**/common/*.c",
        "**/common/*.cc",
        "**/common/*.cpp",
    ]),
    hdrs = glob(["**/common/*.h"])
    + select({
              "windows" : ["cryptonote_basic/portable_binary_archive.hpp",
                           "cryptonote_basic/portable_binary_iarchive.hpp",
                           "cryptonote_basic/portable_binary_oarchive.hpp"]
      }),
    linkopts = [
        "-lssl",
        "-lcrypto",
    ] + select({
             "windows": [],
             "//conditions:default": ["-ldl"],
         }),
    deps = [
        "//src:cncrypto",
        "//src:config",
        "//translations",
        "//contrib/epee:epee",
        "@boost//:chrono",
        "@boost//:date_time",
        "@boost//:filesystem",
        "@boost//:regex",
        "@boost//:system",
        "@boost//:thread",
        "@easy_logging",
        "@libunwind",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
        "@unbound",
        "@libsodium",
    ],
)

# ANOTHER WORKAROUND FOR TESTS. DO NOT USE NORMALLY.
cc_library(
    name = "common_for_tests",
    srcs = [],
    hdrs = ["common/base58.cpp"],
    deps = [],
)

cc_library(
    name = "cryptonote_protocol",
    srcs = glob(["**/cryptonote_protocol/*.cpp"]),
    hdrs = glob(["**/cryptonote_protocol/*.h"]) + glob(["**/cryptonote_protocol/*.inl"]),
    deps = ["//src:p2p"],
)

cc_library(
    name = "p2p",
    srcs = [
        "cryptonote_protocol/levin_notify.h",
        "p2p/net_node.cpp",
        "p2p/net_peerlist.cpp",
    ],
    hdrs = [
        "p2p/net_node.h",
        "p2p/net_node.inl",
        "p2p/net_node_common.h",
        "p2p/net_peerlist.h",
        "p2p/net_peerlist_boost_serialization.h",
        "p2p/p2p_protocol_defs.h",
        "p2p/stdafx.h",
    ],
    deps = [
        "//src:cryptonote_core",
        "//src:net",
        "//src:version",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
        "@boost_extra",
        "@miniupnp//:miniupnpc",
    ],
)

cc_library(
    name = "ringct_basic",
    srcs = [
        "cryptonote_basic/account.h",
        "cryptonote_basic/blobdatatype.h",
        "cryptonote_basic/cryptonote_basic.h",
        "cryptonote_basic/cryptonote_basic_impl.h",
        "cryptonote_basic/cryptonote_format_utils.h",
        "cryptonote_basic/subaddress_index.h",
        "cryptonote_basic/tx_extra.h",
        "serialization/binary_utils.h",
        "device/device.hpp",
        "ringct/bulletproofs.cc",
        "ringct/multiexp.cc",
        "ringct/rctCryptoOps.c",
        "ringct/rctOps.cpp",
        "ringct/rctTypes.cpp",
        "serialization/binary_archive.h",
        "serialization/container.h",
        "serialization/containers.h",
        "serialization/crypto.h",
        "serialization/debug_archive.h",
        "serialization/json_archive.h",
        "serialization/serialization.h",
        "serialization/variant.h",
    ],
    hdrs = [
        "ringct/bulletproofs.h",
        "ringct/multiexp.h",
        "ringct/rctCryptoOps.h",
        "ringct/rctOps.h",
        "ringct/rctTypes.h",
    ],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ] + select({
             "windows": [],
             "//conditions:default": ["-ldl"],
         }),
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src/centralnode:dynamic_critical_values",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
    ],
)

cc_library(
    name = "ringct",
    srcs = ["ringct/rctSigs.cpp"],
    hdrs = ["ringct/rctSigs.h"],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ] + select({
             "windows": [],
             "//conditions:default": ["-ldl"],
         }),
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_basic",
        "//src:device",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
    ],
)

cc_library(
    name = "serialization",
    srcs = [
        "rpc/message_data_structs.h",
        "serialization/json_object.cpp",
    ],
    hdrs = ["serialization/json_object.h"],
    deps = [
        "//contrib/epee",
        "//src:cryptonote_basic",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:version",
        "@boost//:chrono",
        "@boost//:regex",
        "@boost//:system",
        "@boost//:thread",
        "@rapidjson",
    ],
)

cc_library(
    name = "cryptonote_basic",
    srcs = [
        "blockchain_db/blockchain_db.h",
        "cryptonote_basic/account.cpp",
        "cryptonote_basic/cryptonote_basic_impl.cpp",
        "cryptonote_basic/cryptonote_format_utils.cpp",
        "cryptonote_basic/difficulty.cpp",
        "cryptonote_basic/hardfork.cpp",
        "cryptonote_basic/miner.cpp",
        "cryptonote_protocol/enums.h",
        "ringct/rctSigs.h",
        "serialization/binary_utils.h",
        "serialization/crypto.h",
        "serialization/string.h",
        "serialization/variant.h",
    ],
    hdrs = [
        "cryptonote_basic/account.h",
        "cryptonote_basic/account_boost_serialization.h",
        "cryptonote_basic/connection_context.h",
        "cryptonote_basic/cryptonote_basic.h",
        "cryptonote_basic/cryptonote_basic_impl.h",
        "cryptonote_basic/cryptonote_boost_serialization.h",
        "cryptonote_basic/cryptonote_format_utils.h",
        "cryptonote_basic/difficulty.h",
        "cryptonote_basic/events.h",
        "cryptonote_basic/hardfork.h",
        "cryptonote_basic/miner.h",
        "cryptonote_basic/tx_extra.h",
        "cryptonote_basic/verification_context.h",
    ] + select({
        "windows" : ["cryptonote_basic/portable_binary_archive.hpp",
                     "cryptonote_basic/portable_binary_iarchive.hpp",
                     "cryptonote_basic/portable_binary_oarchive.hpp"]
    }),
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:device",
        "//src:hardforks",
        "//src/centralnode:dynamic_critical_values",
        "@boost//:date_time",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
        "@boost_extra",
    ],
)

cc_library(
    name = "device",
    srcs = [
        "cryptonote_basic/account.h",
        "cryptonote_basic/subaddress_index.h",
        "cryptonote_basic/tx_extra.h",
        "cryptonote_core/cryptonote_tx_utils.h",
        "device/device.cpp",
        "device/device_default.cpp",
        "device/device_io_hid.cpp",
        "device/device_ledger.cpp",
        "device/log.cpp",
        "rpc/core_rpc_server_error_codes.h",
        "serialization/pair.h",
        "cryptonote_core/blockchain.h",
        "cryptonote_protocol/cryptonote_protocol_defs.h",
        "rpc/core_rpc_server_commands_defs.h",
        "cryptonote_basic/difficulty.h",
        "rpc/rpc_handler.h",
        "cryptonote_basic/verification_context.h",
        "cryptonote_protocol/enums.h",
        "cryptonote_basic/hardfork.h",
        "blockchain_db/blockchain_db.h",
        "cryptonote_core/tx_pool.h",
        "rpc/message_data_structs.h",
        "ringct/rctSigs.h",
        "cryptonote_basic/cryptonote_boost_serialization.h",
        "blockchain_db/locked_txn.h",
        "common/portable_binary_oarchive.hpp",
        "common/portable_binary_iarchive.hpp",
        "cryptonote_basic/miner.h",
        "cryptonote_core/cryptonote_core_common.h",
        "hardforks/hardforks.h",
        "multisig/multisig.h",
        "crypto/wallet/crypto.h",
        "crypto/wallet/ops.h",
        "wallet/message_store.h",
        "wallet/message_transporter.h",
        "wallet/node_rpc_proxy.h",
        "wallet/wallet2.h",
        "wallet/wallet_errors.h",
        "wallet/wallet_light_rpc.h",
        "wallet/wallet_rpc_helpers.h",
        "checkpoints/checkpoints.h",
    ],
    hdrs = [
        "device/device.hpp",
        "device/device_cold.hpp",
        "device/device_default.hpp",
        "device/device_io.hpp",
        "device/device_io_hid.hpp",
        "device/device_ledger.hpp",
        "device/log.hpp",
    ],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ] + select({
             "windows": [],
             "//conditions:default": ["-ldl"],
         }),
    deps = [
        "//src:cncrypto",
        "//src:ringct_basic",
        "//src:version",
        "//src/blocks",
        "//src/centralnode:dynamic_critical_values",
        "@boost//:serialization",
        "@libhidapi",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
    ],
)

cc_library(
    name = "cryptonote_core",
    srcs = [
        "cryptonote_basic/cryptonote_format_utils.h",
        "cryptonote_basic/fwd.h",
        "cryptonote_core/blockchain.cpp",
        "cryptonote_core/cryptonote_core.cpp",
        "cryptonote_core/cryptonote_tx_utils.cpp",
        "cryptonote_core/tx_pool.cpp",
        "cryptonote_core/tx_sanity_check.cpp",
        "cryptonote_protocol/cryptonote_protocol_defs.h",
        "cryptonote_protocol/cryptonote_protocol_handler_common.h",
        "cryptonote_protocol/fwd.h",
        "p2p/net_node_common.h",
        "p2p/p2p_protocol_defs.h",
        "rpc/core_rpc_server_commands_defs.h",
        "rpc/fwd.h",
        "rpc/message_data_structs.h",
        "rpc/rpc_handler.h",
        "rpc/zmq_pub.h",
    ],
    hdrs = [
        "cryptonote_core/blockchain.h",
        "cryptonote_core/blockchain_storage_boost_serialization.h",
        "cryptonote_core/cryptonote_core.h",
        "cryptonote_core/cryptonote_tx_utils.h",
        "cryptonote_core/i_core_events.h",
        "cryptonote_core/tx_pool.h",
        "cryptonote_core/tx_sanity_check.h",
        "cryptonote_core/cryptonote_core_common.h"
    ],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cncrypto",
        "//src:common",
        "//src:device",
        "//src:net",
        "//src:ringct",
        "//src:version",
        "//src:checkpoints",
        "//src:hardforks",
        "//src:multisig",
        "@boost//:date_time",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
    ],
)

cc_library(
    name = "blockchain_db",
    srcs = [
        "blockchain_db/blockchain_db.cpp",
        "blockchain_db/lmdb/db_lmdb.cpp",
        "blockchain_db/locked_txn.h",
    ],
    hdrs = [
        "blockchain_db/blockchain_db.h",
        "blockchain_db/lmdb/db_lmdb.h",
        "blockchain_db/testdb.h",
    ],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:ringct",
        "@boost//:filesystem",
        "@boost//:thread",
        "@db_drivers",
    ],
)

cc_library(
    name = "wallet",
    srcs = [
        "rpc/core_rpc_server_commands_defs.h",
        "rpc/rpc_payment_costs.h",
        "serialization/pair.h",
        "wallet/message_store.cpp",
        "wallet/message_transporter.cpp",
        "wallet/node_rpc_proxy.cpp",
        "wallet/ringdb.cpp",
        "wallet/wallet2.cpp",
        "wallet/wallet_args.cpp",
        "wallet/wallet_rpc_payments.cpp",
    ],
    hdrs = [
        "wallet/message_store.h",
        "wallet/message_transporter.h",
        "wallet/node_rpc_proxy.h",
        "wallet/ringdb.h",
        "wallet/wallet2.h",
        "wallet/wallet_args.h",
        "wallet/wallet_errors.h",
        "wallet/wallet_rpc_helpers.h",
        "wallet/wallet_rpc_server.h",
        "wallet/wallet_rpc_server_commands_defs.h",
        "wallet/wallet_rpc_server_error_codes.h",
    ],
    deps = [
        "//src:common",
        "//src:cryptonote_core",
        "//src:net",
        "//src:rpc_base",
        "//src/centralnode:dynamic_critical_values",
        "//src/device_trezor",
        "//src/mnemonics",
        "//src:multisig",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:regex",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
        "@db_drivers",
    ],
)

cc_binary(
    name = "denarii_wallet_rpc_server",
    srcs = [
        "wallet/wallet_rpc_server.cpp",
        "wallet/wallet_rpc_server.h",
    ],
    linkopts = [
        "-lssl",
        "-lcrypto",
        "-lcrypt",
        "-ldl",
        "-lpthread",
        "-lboost_system",
        "-lboost_thread",
    ],
    deps = [
        ":wallet",
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_core",
        "//src:rpc_base",
        "//src:version",
        "//src/daemonizer",
        "@boost//:asio_ssl",
        "@boost//:chrono",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_library(
    name = "net",
    srcs = [
        "net/dandelionpp.cpp",
        "net/error.cpp",
        "net/http.cpp",
        "net/i2p_address.cpp",
        "net/parse.cpp",
        "net/socks.cpp",
        "net/socks_connect.cpp",
        "net/tor_address.cpp",
        "net/zmq.cpp",
    ],
    hdrs = [
        "net/dandelionpp.h",
        "net/error.h",
        "net/fwd.h",
        "net/http.h",
        "net/i2p_address.h",
        "net/parse.h",
        "net/socks.h",
        "net/socks_connect.h",
        "net/tor_address.h",
        "net/zmq.h",
    ] + select({
             "windows" : ["net/include/zmq.h"]
         }),
    deps = [
        "//contrib/epee",
        "//src:common",
        "@boost//:asio",
        "@libzmq",
    ],
)

cc_library(
    name = "rpc_base",
    srcs = [
        "rpc/rpc_args.cpp",
        "rpc/rpc_handler.cpp",
        "rpc/rpc_payment_signature.cpp",
    ],
    hdrs = [
        "rpc/rpc_args.h",
        "rpc/rpc_handler.h",
        "rpc/rpc_payment_signature.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:common",
        "//src:cryptonote_core",
        "@boost//:program_options",
        "@boost//:regex",
        "@boost//:thread",
    ],
)

cc_library(
    name = "rpc",
    srcs = [
        "rpc/bootstrap_daemon.cpp",
        "rpc/bootstrap_daemon.h",
        "rpc/bootstrap_node_selector.cpp",
        "rpc/bootstrap_node_selector.h",
        "rpc/core_rpc_server.cpp",
        "rpc/core_rpc_server.h",
        "rpc/core_rpc_server_error_codes.h",
        "rpc/fwd.h",
        "rpc/cryptonote_instantiations.cpp",
        "rpc/nodetool_instantiations.cpp",
        "rpc/rpc_payment.cpp",
        "rpc/rpc_payment.h",
        "rpc/rpc_payment_costs.h",
        "rpc/rpc_version_str.cpp",
    ],
    hdrs = [
        "rpc/rpc_handler.h",
        "rpc/rpc_version_str.h",
    ],
    copts = ["-Wa,-mbig-obj"],
    deps = [
        ":rpc_base",
        "//src:common",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:net",
        "//src:version",
        "@boost//:regex",
        "@boost//:thread",
        "@rapidjson",
    ],
)

cc_library(
    name = "rpc_pub",
    srcs = [
        "rpc/fwd.h",
        "rpc/zmq_pub.cpp",
    ],
    hdrs = ["rpc/zmq_pub.h"],
    deps = [
        "//contrib/epee",
        "//src:cryptonote_basic",
        "//src:net",
        "//src:serialization",
        "@boost//:thread",
        "@rapidjson",
    ],
)

cc_library(
    name = "daemon_messages",
    srcs = [
        "rpc/daemon_messages.cpp",
        "rpc/daemon_rpc_version.h",
        "rpc/message.cpp",
        "rpc/message_data_structs.h",
    ],
    hdrs = [
        "rpc/daemon_messages.h",
        "rpc/message.h",
    ],
    deps = [
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:serialization",
        "//src:version",
        "@rapidjson",
    ],
)

cc_library(
    name = "daemon_rpc_server",
    srcs = [
        "rpc/daemon_handler.cpp",
        "rpc/daemon_rpc_version.h",
        "rpc/message_data_structs.h",
        "rpc/zmq_pub.cpp",
        "rpc/zmq_server.cpp",
    ],
    hdrs = [
        "rpc/daemon_handler.h",
        "rpc/daemon_messages.h",
        "rpc/message.h",
        "rpc/zmq_server.h",
    ],
    deps = [
        ":daemon_messages",
        ":rpc",
        ":rpc_pub",
        "//src:cryptonote_core",
        "//src:cryptonote_protocol",
        "//src:serialization",
        "//src:version",
        "@boost//:chrono",
        "@boost//:regex",
        "@boost//:system",
        "@boost//:thread",
        "@libzmq",
        "@rapidjson",
    ],
)

# DO NOT USE NORMALLY THIS IS JUST A WORKAROUND
cc_library(
    name = "daemon_files_for_test",
    srcs = glob([
        "**/daemon/*.c",
        "**/daemon/*.cpp",
        "**/daemon/*.cc",
    ]),
    hdrs = glob([
        "**/daemon/*.h",
        "**/daemon/*.hpp",
    ]),
    deps = [
        ":daemon_rpc_server",
        "//contrib/epee",
        "//src/daemonizer",
        "@rapidjson",
    ],
)

cc_binary(
    name = "denarii_blockchain_export",
    srcs = [
        "blockchain_utilities/blockchain_export.cpp",
        "blockchain_utilities/blockchain_utilities.h",
        "blockchain_utilities/blocksdat_file.cpp",
        "blockchain_utilities/blocksdat_file.h",
        "blockchain_utilities/bootstrap_file.cpp",
        "blockchain_utilities/bootstrap_file.h",
        "blockchain_utilities/bootstrap_serialization.h",
        "serialization/difficulty_type.h",
        "serialization/json_utils.h",
    ],
    linkopts = [
        "-lssl",
        "-lcrypto",
    ] + select({
        "windows": [],
        "//conditions:default": ["-ldl"],
    }),
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:system",
        "@boost//:thread",
        "@liblzma",
        "@openssl//:libcrypto",
        "@openssl//:libssl",
    ],
)

cc_binary(
    name = "denarii_blockchain_import",
    srcs = [
        "blockchain_utilities/blockchain_import.cpp",
        "blockchain_utilities/blockchain_utilities.h",
        "blockchain_utilities/blocksdat_file.cpp",
        "blockchain_utilities/blocksdat_file.h",
        "blockchain_utilities/bootstrap_file.cpp",
        "blockchain_utilities/bootstrap_file.h",
        "blockchain_utilities/bootstrap_serialization.h",
        "serialization/difficulty_type.h",
        "serialization/json_utils.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "//src/blocks",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
        "@boost//:asio_ssl"
    ],
)

cc_binary(
    name = "denarii_blockchain_blackball",
    srcs = [
        "blockchain_utilities/blockchain_blackball.cpp",
        "blockchain_utilities/blockchain_utilities.h",
        "blockchain_utilities/blocksdat_file.h",
        "blockchain_utilities/bootstrap_file.h",
        "blockchain_utilities/bootstrap_serialization.h",
        "serialization/difficulty_type.h",
    ],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "//src:wallet",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_usage",
    srcs = ["blockchain_utilities/blockchain_usage.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_ancestry",
    srcs = ["blockchain_utilities/blockchain_ancestry.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_prune_know_spent_data",
    srcs = ["blockchain_utilities/blockchain_prune_known_spent_data.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:p2p",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_prune",
    srcs = ["blockchain_utilities/blockchain_prune.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:p2p",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_depth",
    srcs = ["blockchain_utilities/blockchain_depth.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "denarii_blockchain_stats",
    srcs = ["blockchain_utilities/blockchain_stats.cpp"],
    deps = [
        "//contrib/epee",
        "//src:blockchain_db",
        "//src:cryptonote_core",
        "//src:version",
        "@boost//:filesystem",
        "@boost//:thread",
        "@liblzma",
    ],
)

cc_binary(
    name = "cannot_catch_exception",
    srcs = [
        "cannot_catch_exception.cpp",
    ],
    linkopts = [
    ],
    deps = [
        "@libunwind",
    ],
)

cc_binary(
    name = "cannot_catch_boost_interrupt",
    srcs = ["cannot_catch_boost_interrupt.cpp"],
    linkopts = [
        "-llzma",
    ],
    deps = [
        "@boost//:thread",
        "@liblzma",
        "@libunwind",
    ],
)

cc_binary(
    name = "what_is_argv",
    srcs = ["what_is_argv.cpp"],
)

cc_library(
    name = "checkpoints",
    srcs = ["checkpoints/checkpoints.cpp"],
    hdrs = ["checkpoints/checkpoints.h"],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_basic",
        "@boost//:date_time",
        "@boost//:filesystem",
        "@boost//:program_options",
        "@boost//:serialization",
        "@boost//:system",
        "@boost//:thread",
    ],
)

# WORKAROUND TO GET TESTS WORKING DO NOT USE
cc_library(
    name = "checkpoints_for_tests",
    srcs = [],
    hdrs = ["checkpoints/checkpoints.cpp"],
    deps = [],
)

cc_library(
    name = "hardforks",
    srcs = ["hardforks/hardforks.cpp"],
    hdrs = ["hardforks/hardforks.h"],
    deps = ["//src:version"],
)

cc_library(
    name = "multisig",
    srcs = ["multisig/multisig.cpp"],
    hdrs = ["multisig/multisig.h"],
    deps = [
        "//src:cncrypto",
        "//src:common",
        "//src:cryptonote_basic",
        "//src:ringct",
    ],
)
