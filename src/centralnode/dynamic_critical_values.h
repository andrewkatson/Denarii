#ifndef DENARII_DYNAMIC_CRITICAL_VALUES_H
#define DENARII_DYNAMIC_CRITICAL_VALUES_H


#include "Protobuf/TextProto/read_text_proto.h"
#include "src/centralnode/Proto/critical_values.pb.h"

namespace centralnode {
    class dynamic_critical_values {
    public:
        // returns a dynamically calculated block reward or 0 if a connection cannot be made.
        double get_block_reward();

        // returns a dynamically calculated transaction fee or 0 if a connection cannot be made.
        double get_transaction_fee();

        dynamic_critical_values();
        ~dynamic_critical_values();
    };

} // centralnode

#endif //DENARII_DYNAMIC_CRITICAL_VALUES_H
