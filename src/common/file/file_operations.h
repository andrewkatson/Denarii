#pragma once

#include <fstream>
#include <iostream>
#include <string>


namespace file {
  /** Creates a text file */
  void createTextFile(const std::string &path, const std::string &text);
}

