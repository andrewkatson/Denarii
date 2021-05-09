#pragma once

namespace cryptonote {
    /**
    * @brief Callback routine that returns checkpoints data for specific network type
    *
    * @param network network type
    *
    * @return checkpoints data, empty span if there ain't any checkpoints for specific network type
    */
    typedef std::function<const epee::span<const unsigned char>(cryptonote::network_type network)> GetCheckpointsCallback;

    struct test_options {
        const std::pair<uint8_t, uint64_t> *hard_forks;
        const size_t long_term_block_weight_window;
    };
}



