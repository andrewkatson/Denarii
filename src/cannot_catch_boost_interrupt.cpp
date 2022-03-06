
#include <iostream>

#include "boost/thread.hpp"

class Miner {
public:
    inline void worker_thread() {
        try {
            for (int i = 0; i < 1000; i++) {
                std::cout << "Running" << std::endl;
                boost::this_thread::sleep_for(boost::chrono::seconds(10));
            }
        } catch (const boost::thread_interrupted&) {
            std::cout << "Thread interrupted" << std::endl;
        }
    }

    inline void run_thread() {
        boost::thread::attributes m_attrs;
        m_attrs.set_stack_size(5 * 1024 * 1024);

        t = boost::thread(m_attrs, boost::bind(&Miner::worker_thread, this));
        t.interrupt();
        t.join();
    }

    boost::thread t;
};

int main() {

    Miner miner;
    miner.run_thread();

}