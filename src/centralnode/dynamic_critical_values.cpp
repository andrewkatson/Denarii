#include "dynamic_critical_values.h"

using boost::asio::ip::tcp;

namespace centralnode {

    dynamic_critical_values::dynamic_critical_values()
            : m_io_service(), m_work(m_io_service), m_socket(m_io_service), m_io([this]() { m_io_service.run(); }) {

        connected = get_connected();
    }

    dynamic_critical_values::~dynamic_critical_values() {
        m_io_service.stop();
        m_socket.close();
        if (m_io.joinable()) {
            m_io.join();
        }
    }

    uint64_t dynamic_critical_values::get_block_reward() {

        if (!connected) {
            return 0;
        }

        denarii_core::core::CriticalValuesInfoRequest critical_values_request;
        critical_values_request.mutable_requested_values()->add_paths("block_reward");

        common::reactor::Event event;
        event.set_stored_event(critical_values_request.SerializeAsString());

        send(event);

        bool available = wait_for_availability();

        if (!available) {
            return 0;
        }

        common::reactor::Event response_event;

        receive(&response_event);

        denarii_core::core::CriticalValuesInfoResponse critical_values_info_response;

        critical_values_info_response.ParseFromString(response_event.stored_event());

        if (!critical_values_info_response.success()) {
            return 0;
        }

        return critical_values_info_response.values_calculation().block_reward();
    }

    uint64_t dynamic_critical_values::get_transaction_fee() {

        if (!connected) {
            return 0;
        }

        denarii_core::core::CriticalValuesInfoRequest critical_values_request;
        critical_values_request.mutable_requested_values()->add_paths("transaction_fee");

        common::reactor::Event event;
        event.set_stored_event(critical_values_request.SerializeAsString());

        send(event);

        bool available = wait_for_availability();

        if (!available) {
            return 0;
        }

        common::reactor::Event response_event;

        receive(&response_event);

        denarii_core::core::CriticalValuesInfoResponse critical_values_info_response;

        critical_values_info_response.ParseFromString(response_event.stored_event());

        if (!critical_values_info_response.success()) {
            return 0;
        }

        return critical_values_info_response.values_calculation().transaction_fee();
    }

    void dynamic_critical_values::send(const common::reactor::Event& event) {
        AsioOutputStream<boost::asio::ip::tcp::socket> aos(m_socket); // Where m_socket is a instance of boost::asio::ip::tcp::socket
        CopyingOutputStreamAdaptor cos_adp(&aos);

        google::protobuf::io::writeDelimitedTo(event, &cos_adp);
        // Now we have to flush, otherwise the write to the socket won't happen until enough bytes accumulate
        cos_adp.Flush();
    }

    void dynamic_critical_values::receive(common::reactor::Event* event) {

        AsioInputStream<tcp::socket> ais(m_socket);
        CopyingInputStreamAdaptor cis_adp(&ais);

        google::protobuf::io::readDelimitedFrom(&cis_adp, event);
    }

    bool dynamic_critical_values::wait_for_availability() {

        int count = 0;
        while (m_socket.available() == 0 && count < 6) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            count++;
        }

        if (count >= 6) {
            return false;
        }
        return true;
    }

    bool dynamic_critical_values::get_connected() {

        m_socket.open(boost::asio::ip::tcp::v4());
        boost::system::error_code ec;
        m_socket.bind(boost::asio::ip::tcp::endpoint(
                boost::asio::ip::tcp::v4(), 8383), ec);
        if (ec)
        {
            return false;
        }

        // Connect so we can send/receive messages
        boost::asio::ip::tcp::resolver resolver(m_io_service);
        boost::asio::ip::tcp::resolver::iterator resolved_endpoint = resolver.resolve(
                boost::asio::ip::tcp::resolver::query("127.0.0.1", "8484"));
        boost::asio::ip::tcp::resolver::iterator end;
        boost::system::error_code ec2;
        if (resolved_endpoint != end) {
            m_socket.connect(*resolved_endpoint, ec2);

            if (ec2) {
                return false;
            }
        } else {
            return false;
        }

        if (m_socket.is_open()) {
            return true;
        }

        return false;
    }


} // centralnode