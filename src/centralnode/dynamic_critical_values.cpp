#include "dynamic_critical_values.h"

namespace centralnode {

    dynamic_critical_values::dynamic_critical_values() {

    }

    dynamic_critical_values::~dynamic_critical_values() {

    }

    double dynamic_critical_values::get_block_reward() {
      denarii::CriticalValues criticalValues;

      protobuf::keiros::readTextProto("src/centralnode/critical_values.textpb", &criticalValues);

      return criticalValues.block_reward();
    }

    double dynamic_critical_values::get_transaction_fee() {

      denarii::CriticalValues criticalValues;

      protobuf::keiros::readTextProto("src/centralnode/critical_values.textpb", &criticalValues);

      return criticalValues.transaction_fee();
    }


} // centralnode