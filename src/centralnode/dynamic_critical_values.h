#ifndef DENARII_DYNAMIC_CRITICAL_VALUES_H
#define DENARII_DYNAMIC_CRITICAL_VALUES_H

#include <chrono>
#include <thread>

#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/io_service.hpp>
#include <boost/asio/steady_timer.hpp>
#include <boost/asio/streambuf.hpp>
#include <boost/thread/future.hpp>

#include "Reactor/CriticalValuesCalculator/Proto/critical_values_calculation.pb.h"
#include "Reactor/Proto/critical_values_info_request.pb.h"
#include "Reactor/Proto/critical_values_info_response.pb.h"
#include "Reactor/Proto/Event/Base/event.pb.h"
#include "src/net/socks_connect.h"
#include "src/net/parse.h"
#include "src/protobuf/asio_adapting.h"
#include "src/protobuf/protobuf_helpers.h"

namespace centralnode {
    class dynamic_critical_values {
    public:
        // returns a dynamically calculated block reward or 0 if a connection cannot be made.
        uint64_t get_block_reward();

        // returns a dynamically calculated transaction fee or 0 if a connection cannot be made.
        uint64_t get_transaction_fee();

        dynamic_critical_values();
        ~dynamic_critical_values();
    private:

        // Connect the socket to the local endpoint. Returns true if socket is open and false otherwise
        bool get_connected();

        // Send some data through the socket
        void send(const common::reactor::Event& event);

        // Receive some data through the socket
        void receive(common::reactor::Event* event);

        // Wait for some data to be available. Or if five seconds pass time out.
        bool wait_for_availability();

        boost::asio::io_service m_io_service;
        boost::asio::io_service::work m_work;
        boost::thread m_io;
        boost::asio::ip::tcp::socket m_socket;
        bool connected;
    };

} // centralnode

#endif //DENARII_DYNAMIC_CRITICAL_VALUES_H
