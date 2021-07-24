//
// Created by katso on 7/24/2021.
//
#include <boost/program_options/options_description.hpp>
#include <boost/program_options/variables_map.hpp>
#include <string>
#include "src/common/util.h"
#include "contrib/epee/include/net/http_server_impl_base.h"
#include "contrib/epee/include/math_helper.h"
#include "src/wallet/wallet2.h"

#include <boost/format.hpp>
#include <boost/asio/ip/address.hpp>
#include <boost/filesystem/operations.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/preprocessor/stringize.hpp>
#include <cstdint>
#include "contrib/epee/include/include_base_utils.h"
#include "src/wallet/wallet_args.h"
#include "src/common/command_line.h"
#include "src/common/i18n.h"
#include "src/cryptonote_config.h"
#include "src/cryptonote_basic/cryptonote_format_utils.h"
#include "src/cryptonote_basic/account.h"
#include "src/multisig/multisig.h"
#include "src/wallet/wallet_rpc_server_commands_defs.h"
#include "contrib/epee/include/misc_language.h"
#include "contrib/epee/include/string_coding.h"
#include "contrib/epee/include/string_tools.h"
#include "src/crypto/hash.h"
#include "src/mnemonics/electrum-words.h"
#include "src/rpc/rpc_args.h"
#include "src/rpc/core_rpc_server_commands_defs.h"
#include "src/daemonizer/daemonizer.h"
#include "src/version.h"

int main() {
  return 0;
}