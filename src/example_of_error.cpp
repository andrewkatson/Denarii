#include <stdexcept>
#include <vector>
#include <iostream>
#include <ostream>
#include <sstream>

namespace tools {
    namespace error {

        template<typename Base>
        struct wallet_error_base : public Base {
            const std::string &location() const { return m_loc; }

            std::string to_string() const {
                std::ostringstream ss;
                ss << m_loc << ':' << typeid(*this).name() << ": " << Base::what();
                return ss.str();
            }

        protected:
            wallet_error_base(std::string &&loc, const std::string &message)
                    : Base(message), m_loc(loc) {
            }

        private:
            std::string m_loc;
        };

        typedef wallet_error_base<std::logic_error> wallet_logic_error;

        struct wallet_rpc_error : public wallet_logic_error {
            const std::string &request() const { return m_request; }

            std::string to_string() const {
                std::ostringstream ss;
                ss << wallet_logic_error::to_string() << ", request = " << m_request;
                return ss.str();
            }

        protected:
            explicit wallet_rpc_error(std::string &&loc, const std::string &message, const std::string &request)
                    : wallet_logic_error(std::move(loc), message), m_request(request) {
            }

        private:
            std::string m_request;
        };

        struct wallet_generic_rpc_error : public wallet_rpc_error {
            explicit wallet_generic_rpc_error(std::string &&loc, const std::string &request, const std::string &status)
                    : wallet_rpc_error(std::move(loc), std::string("error in ") + request + " RPC: " + status, request),
                      m_status(status) {
            }

            const std::string &status() const { return m_status; }

        private:
            const std::string m_status;
        };

        // Base case for the variadic template recursion
        template<typename TException>
        void throw_wallet_ex(std::string&& loc) {
            TException e(std::move(loc));
            std::cout << e.to_string();
            throw e;
        }

        // Recursive variadic template function to accept a variable number of string arguments
        template<typename TException, typename... Args>
        void throw_wallet_ex(std::string&& loc, const Args& ... args) {
            TException e(std::move(loc), args...);
            std::cout << e.to_string();
            throw e;
        }
    }
}

#define THROW_ON_RPC_RESPONSE_ERROR(r, error, res, method, ...) \
  do { \
    THROW_WALLET_EXCEPTION_IF(res.status != "ok", ## __VA_ARGS__); \
  } while(0)

#define THROW_ON_RPC_RESPONSE_ERROR_GENERIC(r, err, res, method) \
  THROW_ON_RPC_RESPONSE_ERROR(r, err, res, method, tools::error::wallet_generic_rpc_error, method, res.status)

#define STRINGIZE_DETAIL(x) #x
#define STRINGIZE(x) STRINGIZE_DETAIL(x)

#define THROW_WALLET_EXCEPTION_IF(cond, err_type, ...)                                                      \
  if (cond)                                                                                                 \
  {                                                                                                         \
    std::cerr << #cond << ". THROW EXCEPTION: " << #err_type;                                              \
    tools::error::throw_wallet_ex<err_type>(std::string(__FILE__ ":" STRINGIZE(__LINE__)), ## __VA_ARGS__); \
  }

  struct result {
    result(const std::string& status) : status(status) {

    }
    std::string status;
};

int main() {
    result res("ok");
    THROW_ON_RPC_RESPONSE_ERROR_GENERIC(true, {}, res, "rpc_access_submit_nonce");
    return 0;
}