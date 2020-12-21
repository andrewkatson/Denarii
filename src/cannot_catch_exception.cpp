

#include <iostream>
#include <stdexcept>
#include <system_error>
#include <string>
#include <vector>
#include <sstream>


template<typename Base>
struct wallet_error_base : public Base
{
    const std::string& location() const { return m_loc; }

    std::string to_string() const
    {
        std::ostringstream ss;
        ss << m_loc << ':' << typeid(*this).name() << ": " << Base::what();
        return ss.str();
    }

protected:
    wallet_error_base(std::string&& loc, const std::string& message)
            : Base(message)
            , m_loc(loc)
    {
    }

private:
    std::string m_loc;
};


typedef wallet_error_base<std::runtime_error> wallet_runtime_error;
//----------------------------------------------------------------------------------------------------
struct wallet_internal_error : public wallet_runtime_error
{
    explicit wallet_internal_error(std::string&& loc, const std::string& message)
            : wallet_runtime_error(std::move(loc), message)
    {
    }
};

template<typename TException, typename... TArgs>
void throw_wallet_ex(std::string&& loc, const TArgs&... args)
{
    TException e(std::move(loc), args...);
    throw e;
}

#define STRINGIZE_DETAIL(x) #x
#define STRINGIZE(x) STRINGIZE_DETAIL(x)

#define THROW_WALLET_EXCEPTION(err_type, ...)                                                               \
  do {                                                                                                      \
    throw_wallet_ex<err_type>(std::string(__FILE__ ":" STRINGIZE(__LINE__)), ## __VA_ARGS__);               \
  } while(0)                                                                                                \



int main() {

  try {
      THROW_WALLET_EXCEPTION(wallet_internal_error, "invalid password");
  }  catch (const std::exception& ex) {
      std::cout << "Caught" << std::endl;
  }

  return 0;
}