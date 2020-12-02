package(default_visibility = ["//visibility:public"])

cc_test(
    name = "core_tests",
    srcs = glob(["*.h"]) + glob(["*.cpp"]),
    copts = ["--generate_and_play_test_data"],
    deps = [
        "//contrib/epee",
        "//src:version",
        "//src/cryptonote_core",
        "//src/device",
        "//src/multisig",
        "//src/p2p",
        "//src/wallet",
    ],
)
