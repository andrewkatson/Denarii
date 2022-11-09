#include "file_operations.h"

namespace file {
    void createTextFile(const std::string &path, const std::string &text) {
      std::ofstream ofs;
      ofs.open(path, std::ofstream::out | std::ofstream::app);

      ofs << text;

      ofs.close();
    }
}