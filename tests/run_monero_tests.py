# This file runs any monero tests that are done through commands in CMAKE. The ones that are run with gtest do not need this
# and have to be run manually
import os
import subprocess

# NEED TO FILL THIS IN WITH YOUR PATH TO DENARII FOR THIS TO WORK SORRY
workspace_path = "/home/andrew/denarii"

failed_tests = []


def report_status_of_test(process, testname):
    if process.returncode == 0:
        print(f"\nTest {testname} passed\n")
    else:
        print(f"\nTest {testname} failed\n")
        failed_tests.append(testname)


def test_block_weight():
    block_weight_py_path = workspace_path + "/bazel-bin/tests/block_weight/block_weight_py"
    block_weight_path = workspace_path + "/bazel-bin/tests/block_weight/block_weight"

    # run compare
    compare_command = "bazel run tests/block_weight:compare -- " + block_weight_py_path + " " + block_weight_path
    compare_proc = subprocess.Popen(compare_command, shell=True, stdout=subprocess.PIPE)
    compare_proc.wait()
    report_status_of_test(compare_proc, "block_weight:compare")


def test_core_proxy():
    # run core proxy
    core_proxy_command = "bazel run tests/core_proxy:core_proxy"
    core_proxy_proc = subprocess.Popen(core_proxy_command, shell=True, stdout=subprocess.PIPE)
    core_proxy_proc.wait()
    report_status_of_test(core_proxy_proc, "core_proxy:core_proxy")


def test_core_tests():
    # run core tests
    core_tests_command = "bazel run tests/core_tests:core_tests -- --generate_and_play_test_data"
    core_tests_proc = subprocess.Popen(core_tests_command, shell=True, stdout=subprocess.PIPE)
    core_tests_proc.wait()
    report_status_of_test(core_tests_proc, "core_tests:core_tests")


def test_crypto():
    tests_path = workspace_path + "/tests/crypto/tests.txt"

    # run crypto
    crypto_command = "bazel run tests/crypto:cnccrypto_tests -- " + tests_path
    crypto_proc = subprocess.Popen(crypto_command, shell=True, stdout=subprocess.PIPE)
    crypto_proc.wait()
    report_status_of_test(crypto_proc, "crypto:crypto")

    # run cnv4-jit-tests
    cnv_command = "bazel run tests/crypto:cnv4_jit_tests -- 1788000 1789000"
    cnv_proc = subprocess.Popen(cnv_command, shell=True, stdout=subprocess.PIPE)
    cnv_proc.wait()
    report_status_of_test(cnv_proc, "crypto:cnv4_jit_tests")


def test_difficulty():
    data_path = workspace_path + "/tests/difficulty/data.txt"
    difficulty_tests_command = "bazel run tests/difficulty:difficulty -- " + data_path
    difficulty_tests_proc = subprocess.Popen(difficulty_tests_command, shell=True, stdout=subprocess.PIPE)
    difficulty_tests_proc.wait()
    report_status_of_test(difficulty_tests_proc, "difficulty:difficulty")

    gen_wide_python_path = workspace_path + "/tests/difficulty/gen_wide_data.py"
    difficulty_tests_path = workspace_path + "/bazel-bin/tests/difficulty/difficulty"
    wide_data_path = workspace_path + "/tests/difficulty/wide_data.txt"
    wide_difficulty_command = "bazel run tests/difficulty:wide_difficulty -- python3 " + gen_wide_python_path + " " + difficulty_tests_path + " " + wide_data_path
    wide_difficulty_proc = subprocess.Popen(wide_difficulty_command, shell=True, stdout=subprocess.PIPE)
    wide_difficulty_proc.wait()
    report_status_of_test(wide_difficulty_proc, "difficulty:wide_difficulty")


def test_functional_tests():
    # Monero doesn't run these
    # functional_tests_command = "bazel run tests/functional_tests:functional_tests"
    # functional_tests_proc = subprocess.Popen(functional_tests_command, shell=True, stdout=subprocess.PIPE)
    # functional_tests_proc.wait()
    # report_status_of_test(functional_tests_proc, "functional_tests:functional_tests")

    # Monero doesn't run these
    # make_test_signature_command = "bazel run tests/functional_tests:make_test_signature"
    # make_test_signature_proc = subprocess.Popen(make_test_signature_command, shell=True, stdout=subprocess.PIPE)
    # make_test_signature_proc.wait()
    # report_status_of_test(make_test_signature_proc, "functional_tests:make_test_signature")

    current_path = workspace_path + "/tests/functional_tests"
    binary_path = workspace_path + "/bazel-bin/src"
    functional_tests_rpc_command = "bazel run tests/functional_tests:functional_tests_rpc -- python3 " + current_path + " " + binary_path + " all"
    functional_tests_rpc_proc = subprocess.Popen(functional_tests_rpc_command, shell=True, stdout=subprocess.PIPE)
    functional_tests_rpc_proc.wait()
    report_status_of_test(functional_tests_rpc_proc, "functional_tests:functional_tests_rpc")

    source_path = workspace_path
    check_missing_command = "bazel run tests/functional_tests:check_missing_rpc_methods -- " + source_path
    check_missing_proc = subprocess.Popen(check_missing_command, shell=True, stdout=subprocess.PIPE)
    check_missing_proc.wait()
    report_status_of_test(check_missing_proc, "functional_tests:check_missing_rpc_methods")


def test_fuzz():
    block_fuzz_tests_command = "bazel run tests/fuzz:block_fuzz_tests"
    functional_tests_proc = subprocess.Popen(block_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    functional_tests_proc.wait()
    report_status_of_test(functional_tests_proc, "fuzz:block_fuzz_tests")

    transaction_fuzz_tests_command = "bazel run tests/fuzz:transaction_fuzz_tests"
    transaction_fuzz_tests_proc = subprocess.Popen(transaction_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    transaction_fuzz_tests_proc.wait()
    report_status_of_test(transaction_fuzz_tests_proc, "fuzz:transaction_fuzz_tests")

    signature_fuzz_tests_command = "bazel run tests/fuzz:signature_fuzz_tests"
    signature_fuzz_tests_proc = subprocess.Popen(signature_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    signature_fuzz_tests_proc.wait()
    report_status_of_test(signature_fuzz_tests_proc, "fuzz:signature_fuzz_tests")

    cold_outputs_fuzz_tests_command = "bazel run tests/fuzz:cold_outputs_fuzz_tests"
    cold_outputs_fuzz_tests_proc = subprocess.Popen(cold_outputs_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    cold_outputs_fuzz_tests_proc.wait()
    report_status_of_test(cold_outputs_fuzz_tests_proc, "fuzz:cold_outputs_fuzz_tests")

    cold_transaction_fuzz_tests_command = "bazel run tests/fuzz:cold_transaction_fuzz_tests"
    cold_transaction_fuzz_tests_proc = subprocess.Popen(cold_transaction_fuzz_tests_command, shell=True,
                                                        stdout=subprocess.PIPE)
    cold_transaction_fuzz_tests_proc.wait()
    report_status_of_test(cold_transaction_fuzz_tests_proc, "fuzz:cold_transaction_fuzz_tests")

    load_from_binary_fuzz_tests_command = "bazel run tests/fuzz:load_from_binary_fuzz_tests"
    load_from_binary_fuzz_tests_proc = subprocess.Popen(load_from_binary_fuzz_tests_command, shell=True,
                                                        stdout=subprocess.PIPE)
    load_from_binary_fuzz_tests_proc.wait()
    report_status_of_test(load_from_binary_fuzz_tests_proc, "fuzz:load_from_binary_fuzz_tests")

    load_from_json_fuzz_tests_command = "bazel run tests/fuzz:load_from_json_fuzz_tests"
    load_from_json_fuzz_tests_proc = subprocess.Popen(load_from_json_fuzz_tests_command, shell=True,
                                                      stdout=subprocess.PIPE)
    load_from_json_fuzz_tests_proc.wait()
    report_status_of_test(load_from_json_fuzz_tests_proc, "fuzz:load_from_json_fuzz_tests")

    base58_fuzz_tests_command = "bazel run tests/fuzz:base58_fuzz_tests"
    base58_fuzz_tests_proc = subprocess.Popen(base58_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    base58_fuzz_tests_proc.wait()
    report_status_of_test(base58_fuzz_tests_proc, "fuzz:base58_fuzz_tests")

    parse_url_fuzz_tests_command = "bazel run tests/fuzz:parse_url_fuzz_tests"
    parse_url_fuzz_tests_proc = subprocess.Popen(parse_url_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    parse_url_fuzz_tests_proc.wait()
    report_status_of_test(parse_url_fuzz_tests_proc, "fuzz:parse_url_fuzz_tests")

    http_client_fuzz_tests_command = "bazel run tests/fuzz:http_client_fuzz_tests"
    http_client_fuzz_tests_proc = subprocess.Popen(http_client_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    http_client_fuzz_tests_proc.wait()
    report_status_of_test(http_client_fuzz_tests_proc, "fuzz:http_client_fuzz_tests")

    levin_fuzz_tests_command = "bazel run tests/fuzz:levin_fuzz_tests"
    levin_fuzz_tests_proc = subprocess.Popen(levin_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    levin_fuzz_tests_proc.wait()
    report_status_of_test(levin_fuzz_tests_proc, "fuzz:levin_fuzz_tests")

    bulletproof_fuzz_tests_command = "bazel run tests/fuzz:bulletproof_fuzz_tests"
    bulletproof_fuzz_tests_proc = subprocess.Popen(bulletproof_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    bulletproof_fuzz_tests_proc.wait()
    report_status_of_test(bulletproof_fuzz_tests_proc, "fuzz:bulletproof_fuzz_tests")

    tx_extra_fuzz_tests_command = "bazel run tests/fuzz:tx_extra_fuzz_tests"
    tx_extra_fuzz_tests_proc = subprocess.Popen(tx_extra_fuzz_tests_command, shell=True, stdout=subprocess.PIPE)
    tx_extra_fuzz_tests_proc.wait()
    report_status_of_test(tx_extra_fuzz_tests_proc, "fuzz:tx_extra_fuzz_tests")


def test_hash():
    flavors = ["fast", "slow", "slow-1", "slow-2", "slow-4", "tree", "extra-blake", "extra-groestl",
               "extra-jh", "extra-skein"]

    for flavor in flavors:
        text_file_path = workspace_path + "/tests/hash/tests-" + flavor + ".txt"
        flavor_command = "bazel run tests/hash:hash_tests -- " + flavor + " " + text_file_path
        flavor_proc = subprocess.Popen(flavor_command, shell=True, stdout=subprocess.PIPE)
        flavor_proc.wait()
        report_status_of_test(flavor_proc, "hash:" + flavor)

    hash_variant_command = "bazel run tests/hash:hash_tests -- " + "variant2_int_sqrt"
    hash_variant_proc = subprocess.Popen(hash_variant_command, shell=True, stdout=subprocess.PIPE)
    hash_variant_proc.wait()
    report_status_of_test(hash_variant_proc, "hash:hash_variant")


def test_performance_tests():
    performance_tests_command = "bazel run tests/performance_tests:performance_tests"
    performance_tests_proc = subprocess.Popen(performance_tests_command, shell=True, stdout=subprocess.PIPE)
    performance_tests_proc.wait()
    report_status_of_test(performance_tests_proc, "performance_tests:performance_tests")


def test_top_level():
    benchmark_command = "bazel run tests:benchmark"
    benchmark_proc = subprocess.Popen(benchmark_command, shell=True, stdout=subprocess.PIPE)
    benchmark_proc.wait()
    report_status_of_test(benchmark_proc, "top_level:benchmark")

    hash_tests_command = "bazel run tests:hash_tests"
    hash_tests_proc = subprocess.Popen(hash_tests_command, shell=True, stdout=subprocess.PIPE)
    hash_tests_proc.wait()
    report_status_of_test(hash_tests_proc, "top_level:hash_tests")


os.chdir(workspace_path)
test_block_weight()
# Monero doesn't run these
# test_core_proxy()
test_core_tests()
test_crypto()
test_difficulty()
test_functional_tests()
# Monero doesnt run these
# test_fuzz()
test_hash()
# Monero doesnt run these
# test_performance_tests()
test_top_level()

print("\n\n\n\n\n\n")
if len(failed_tests) == 0:
    print("All tests passed!")
else:
    print("Some tests failed")
    print(failed_tests)