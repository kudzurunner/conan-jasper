#include <iostream>
#include <string>
#include <jasper/jas_version.h>
#include <jasper/jas_init.h>

int main() {
    std::cout << "JasPer version: " << JAS_VERSION << std::endl;

    if(jas_init()) {
        std::cout << "Can't initialize JasPer" << std::endl;
        return 1;
    }

    jas_cleanup();
    return 0;
}
