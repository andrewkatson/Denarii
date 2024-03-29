// Copyright (c) 2006-2013, Andrey N. Sabelnikov, www.sabelnikov.net
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
// * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above copyright
// notice, this list of conditions and the following disclaimer in the
// documentation and/or other materials provided with the distribution.
// * Neither the name of the Andrey N. Sabelnikov nor the
// names of its contributors may be used to endorse or promote products
// derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER  BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//


#ifndef _MLOG_H_
#define _MLOG_H_

#include <time.h>
#include <atomic>
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include "contrib/epee/include/string_tools.h"
#include "contrib/epee/include/misc_os_dependent.h"
#include "contrib/epee/include/misc_log_ex.h"

#ifdef _WIN32
#include <io.h>
#ifndef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING  0x0004
#endif
#endif


#undef MONERO_DEFAULT_LOG_CATEGORY
#define MONERO_DEFAULT_LOG_CATEGORY "logging"

#define MLOG_BASE_FORMAT "%datetime{%Y-%M-%d %H:%m:%s.%g}\t%thread\t%level\t%logger\t%loc\t%msg"

#define MLOG_LOG(x) MLOG_GREEN(x)

using namespace epee;

static std::string generate_log_filename(const char *base)
{
  std::string filename(base);
  static unsigned int fallback_counter = 0;
  char tmp[200];
  struct tm tm;
  time_t now = time(NULL);
  if (!epee::misc_utils::get_gmt_time(now, tm))
    snprintf(tmp, sizeof(tmp), "part-%u", ++fallback_counter);
  else
    strftime(tmp, sizeof(tmp), "%Y-%m-%d-%H-%M-%S", &tm);
  tmp[sizeof(tmp) - 1] = 0;
  filename += "-";
  filename += tmp;
  return filename;
}

std::string mlog_get_default_log_path(const char *default_filename)
{
  std::string process_name = epee::string_tools::get_current_module_name();
  std::string default_log_folder = epee::string_tools::get_current_module_folder();
  std::string default_log_file = process_name;
  std::string::size_type a = default_log_file.rfind('.');
  if ( a != std::string::npos )
    default_log_file.erase( a, default_log_file.size());
  if ( ! default_log_file.empty() )
    default_log_file += ".log";
  else
    default_log_file = default_filename;

  return (boost::filesystem::path(default_log_folder) / boost::filesystem::path(default_log_file)).string();
}

#ifdef WIN32
bool EnableVTMode()
{
  // Set output mode to handle virtual terminal sequences
  HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
  if (hOut == INVALID_HANDLE_VALUE)
  {
    return false;
  }

  DWORD dwMode = 0;
  if (!GetConsoleMode(hOut, &dwMode))
  {
    return false;
  }

  dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
  if (!SetConsoleMode(hOut, dwMode))
  {
    return false;
  }
  return true;
}
#endif

void mlog_configure(const std::string &filename_base, bool console, const std::size_t max_log_file_size, const std::size_t max_log_files)
{

    try 
    {
        auto logger = spdlog::basic_logger_mt("basic_logger", filename_base);
    }
    catch (const spdlog::spdlog_ex &ex)
    {
        std::cout << "Log init failed: " << ex.what() << std::endl;
    }

#ifdef WIN32
  EnableVTMode();
#endif
}

void mlog_set_categories(const char *categories)
{
  std::string new_categories;
  if (*categories)
  {
    if (*categories == '+')
    {
      ++categories;
      new_categories = mlog_get_categories(log_level);
      if (*categories)
      {
        if (!new_categories.empty())
          new_categories += ",";
        new_categories += categories;
      }
    }
    else if (*categories == '-')
    {
      ++categories;
      new_categories = mlog_get_categories(log_level);
      std::vector<std::string> single_categories;
      boost::split(single_categories, categories, boost::is_any_of(","), boost::token_compress_on);
      for (const std::string &s: single_categories)
      {
        size_t pos = new_categories.find(s);
        if (pos != std::string::npos)
          new_categories = new_categories.erase(pos, s.size());
      }
    }
    else
    {
      new_categories = categories;
    }
  }
}


std::string mlog_get_default_categories(int level)
{
  return mlog_get_categories(level);
}

std::string mlog_get_categories(int level)
{
  switch(level) {
    case 0:
      return "FATAL";
    case 1:
      return "FATAL,ERROR";
    case 2:
      return "FATAL,ERROR,WARNING";
    case 3:
      return "FATAL,ERROR,WARNING,INFO";
    case 4:
      return "FATAL,ERRER,WARNING,INFO,DEBUG";
    case 5: 
      return "FATAL,ERROR,WARNING,INFO,DEBUG,TRACE";
    default: 
      return "FATAL";
  }
}

// maps epee style log level to new logging system
void mlog_set_log_level(int level)
{
  log_level = level;

  switch(log_level) {
    case 0:
      spdlog::set_level(spdlog::level::critical); 
      break;
    case 1:
      spdlog::set_level(spdlog::level::err); 
    case 2:
      spdlog::set_level(spdlog::level::warn); 
    case 3:
      spdlog::set_level(spdlog::level::info); 
    case 4:
      spdlog::set_level(spdlog::level::debug); 
    case 5: 
      spdlog::set_level(spdlog::level::trace); 
    default: 
      spdlog::set_level(spdlog::level::critical); 
  }
}

void mlog_set_log(const char *log)
{
  long level;
  char *ptr = NULL;

  if (!*log)
  {
    mlog_set_categories(log);
    return;
  }
  level = strtol(log, &ptr, 10);
  if (ptr && *ptr)
  {
    // we can have a default level, eg, 2,foo:ERROR
    if (*ptr == ',') {
      std::string new_categories = std::string(mlog_get_default_categories(level)) + ptr;
      mlog_set_categories(new_categories.c_str());
    }
    else {
      mlog_set_categories(log);
    }
  }
  if (level >= 0 && level <= 5)
  {
    mlog_set_log_level(level);
  }
  else
  {
    MERROR("Invalid numerical log level: " << log);
  }
}

namespace epee
{

bool is_stdout_a_tty()
{
  static std::atomic<bool> initialized(false);
  static std::atomic<bool> is_a_tty(false);

  if (!initialized.load(std::memory_order_acquire))
  {
#if defined(WIN32)
    is_a_tty.store(0 != _isatty(_fileno(stdout)), std::memory_order_relaxed);
#else
    is_a_tty.store(0 != isatty(fileno(stdout)), std::memory_order_relaxed);
#endif
    initialized.store(true, std::memory_order_release);
  }

  return is_a_tty.load(std::memory_order_relaxed);
}

void set_console_color(int color, bool bright)
{
  if (!is_stdout_a_tty())
    return;

  switch(color)
  {
  case console_color_default:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE| (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;37m";
      else
        std::cout << "\033[0m";
#endif
    }
    break;
  case console_color_white:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;37m";
      else
        std::cout << "\033[0;37m";
#endif
    }
    break;
  case console_color_red:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_RED | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;31m";
      else
        std::cout << "\033[0;31m";
#endif
    }
    break;
  case console_color_green:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_GREEN | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;32m";
      else
        std::cout << "\033[0;32m";
#endif
    }
    break;

  case console_color_blue:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_BLUE | FOREGROUND_INTENSITY);//(bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;34m";
      else
        std::cout << "\033[0;34m";
#endif
    }
    break;

  case console_color_cyan:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_GREEN | FOREGROUND_BLUE | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;36m";
      else
        std::cout << "\033[0;36m";
#endif
    }
    break;

  case console_color_magenta:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_BLUE | FOREGROUND_RED | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;35m";
      else
        std::cout << "\033[0;35m";
#endif
    }
    break;

  case console_color_yellow:
    {
#ifdef WIN32
      HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
      SetConsoleTextAttribute(h_stdout, FOREGROUND_RED | FOREGROUND_GREEN | (bright ? FOREGROUND_INTENSITY:0));
#else
      if(bright)
        std::cout << "\033[1;33m";
      else
        std::cout << "\033[0;33m";
#endif
    }
    break;

  }
}

void reset_console_color() {
  if (!is_stdout_a_tty())
    return;

#ifdef WIN32
  HANDLE h_stdout = GetStdHandle(STD_OUTPUT_HANDLE);
  SetConsoleTextAttribute(h_stdout, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
#else
  std::cout << "\033[0m";
  std::cout.flush();
#endif
}

}


#define DEFLOG(fun,lev) \
  bool m##fun(const char *category, const char *fmt, ...) { va_list ap; va_start(ap, fmt); bool ret = true; log_level = lev; va_end(ap); return ret; }

DEFLOG(error, 1)
DEFLOG(warning, 2)
DEFLOG(info, 3)
DEFLOG(debug, 4)
DEFLOG(trace, 5)

#undef DEFLOG

#endif //_MLOG_H_
