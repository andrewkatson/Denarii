
#include <iostream>
#include <chrono>
#include <thread>

int main(int argc, char** argv) {	
 std::cout << "HERE" << std::endl;
 std::this_thread::sleep_for(std::chrono::seconds(1));
 return 0;
}