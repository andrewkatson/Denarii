#include <iostream>


template <class T>
void print(T && t) {
    std::cout << t << std::endl;
}

int main() {
    print(uint64_t(10));
}