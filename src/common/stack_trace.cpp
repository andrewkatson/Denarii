// Copyright (c) 2016-2020, The Monero Project
//
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without modification, are
// permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this list of
//    conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice, this list
//    of conditions and the following disclaimer in the documentation and/or other
//    materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its contributors may be
//    used to endorse or promote products derived from this software without specific
//    prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
// THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
// STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
// THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#if !defined __GNUC__ || defined __MINGW32__ || defined __MINGW64__ || defined __ANDROID__
#define USE_UNWIND
#else
#define ELPP_FEATURE_CRASH_LOG 1
#endif
#include "easylogging++.h"

#include <iomanip>
#include <stdexcept>
#ifdef USE_UNWIND
#define UNW_LOCAL_ONLY
#ifndef _WIN32
#include <libunwind.h>
#endif
#ifndef _WIN32
#include <cxxabi.h>
#endif
#endif
#ifndef STATICLIB
#ifndef _WIN32
#include <dlfcn.h>
#endif
#endif
#include <boost/algorithm/string.hpp>
#include "src/common/stack_trace.h"
#include "contrib/epee/include/misc_log_ex.h"

#undef MONERO_DEFAULT_LOG_CATEGORY
#define MONERO_DEFAULT_LOG_CATEGORY "stacktrace"

#ifndef _WIN32
#define ST_LOG(x) \
  do { \
    auto elpp = ELPP; \
    if (elpp) { \
      CINFO(el::base::Writer,el::base::DispatchAction::FileOnlyLog,MONERO_DEFAULT_LOG_CATEGORY) << x; \
    } \
    else { \
      std::cout << x << std::endl; \
    } \
  } while(0)
#endif
// from https://stackoverflow.com/questions/11665829/how-can-i-print-stack-trace-for-caught-exceptions-in-c-code-injection-in-c

// The decl of __cxa_throw in /usr/include/.../cxxabi.h uses
// 'std::type_info *', but GCC's built-in protype uses 'void *'.
#ifdef __clang__
#define CXA_THROW_INFO_T std::type_info
#else // !__clang__
#define CXA_THROW_INFO_T void
#endif // !__clang__

#ifndef _WIN32
#ifdef STATICLIB
#define CXA_THROW __wrap___cxa_throw
extern "C"
__attribute__((noreturn))
void __real___cxa_throw(void *ex, CXA_THROW_INFO_T *info, void (*dest)(void*));
#else // !STATICLIB
#define CXA_THROW __cxa_throw
extern "C"
typedef
#ifdef __clang__ // only clang, not GCC, lets apply the attr in typedef
__attribute__((noreturn))
#endif // __clang__
void (cxa_throw_t)(void *ex, CXA_THROW_INFO_T *info, void (*dest)(void*));
#endif // !STATICLIB
extern "C"
#ifdef _WIN32
__declspec(noreturn)
#else
__attribute__((noreturn))
#endif
#endif

#ifndef _WIN32
void CXA_THROW(void *ex, CXA_THROW_INFO_T *info, void (*dest)(void*))
{
	
// I dont know how this function ever worked on Windows so just disable it entirely. Otherwise we just crash.
#ifndef _WIN32

  int status;

  char *dsym = abi::__cxa_demangle(((const std::type_info*)info)->name(), NULL, NULL, &status);

  tools::log_stack_trace((std::string("Exception: ")+((!status && dsym) ? dsym : (const char*)info)).c_str());

  free(dsym);

#ifndef STATICLIB
#ifndef __clang__ // for GCC the attr can't be applied in typedef like for clang
#ifndef _WIN32
  __attribute__((noreturn))
#endif
#endif // !__clang__
   cxa_throw_t *__real___cxa_throw = (cxa_throw_t*)dlsym(RTLD_NEXT, "__cxa_throw");
   __real___cxa_throw(ex, info, dest);

#endif  // !STATICLIB
}
#endif
namespace
{
  std::string stack_trace_log;
}

namespace tools
{

#ifndef __clang__
void set_stack_trace_log(const std::string &log)
{
  stack_trace_log = log;
}

void log_stack_trace(const char *msg)
{
#if defined(USE_UNWIND) && !defined(_WIN32)
  unw_context_t ctx;
  unw_cursor_t cur;
  unw_word_t ip, off;
  unsigned level;
  char sym[512], *dsym;
  int status;
  const char *log = stack_trace_log.empty() ? NULL : stack_trace_log.c_str();
#endif

#ifndef _WIN32
  if (msg)
    ST_LOG(msg);
  ST_LOG("Unwound call stack:");
#else 
  std::cout << msg << std::endl;
  std::cout << "Unwound call stack:" << std::endl;
#endif

#if defined(USE_UNWIND) && !defined(_WIN32)
  if (unw_getcontext(&ctx) < 0) {
    ST_LOG("Failed to create unwind context");
    return;
  }
  if (unw_init_local(&cur, &ctx) < 0) {
    ST_LOG("Failed to find the first unwind frame");
    return;
  }
  for (level = 1; level < 999; ++level) { // 999 for safety
    int ret = unw_step(&cur);
    if (ret < 0) {
      ST_LOG("Failed to find the next frame");
      return;
    }
    if (ret == 0)
      break;
    if (unw_get_reg(&cur, UNW_REG_IP, &ip) < 0) {
      ST_LOG("  " << std::setw(4) << level);
      continue;
    }
    if (unw_get_proc_name(&cur, sym, sizeof(sym), &off) < 0) {
      ST_LOG("  " << std::setw(4) << level << std::setbase(16) << std::setw(20) << "0x" << ip);
      continue;
    }
    dsym = abi::__cxa_demangle(sym, NULL, NULL, &status);

    ST_LOG("  " << std::setw(4) << level << std::setbase(16) << std::setw(20) << "0x" << ip << " " << (!status && dsym ? dsym : sym) << " + " << "0x" << off);
    free(dsym);
  }
#elif !defined(_WIN32)
  std::stringstream ss;
  ss << el::base::debug::StackTrace();
  std::vector<std::string> lines;
  std::string s = ss.str();
  boost::split(lines, s, boost::is_any_of("\n"));
  
  for (const auto &line: lines) {
    ST_LOG(line);
  }
#endif
}
#else 
void set_stack_trace_log(const std::string &log) {
  // No op because mac isn't playing nice with stack traces during runtime.
}

void log_stack_trace(const char *msg) {
  // No op because mac isn't play nice with stack traces during runtime.
}
#endif
#endif

// FROM: rioki.org/2017/01/09/windows_stacktrace.html
//
// Debug Helpers
// 
// Copyright (c) 2015 - 2017 Sean Farrell <sean.farrell@rioki.org>
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.
// 

#ifdef _WIN32
namespace tools {
namespace dbg
{    
#define DBG_TRACE(MSG, ...)  trace(MSG, ## __VA_ARGS__)

#define DBG_SOFT_ASSERT(COND) if ((COND) == false) { \
                                  DBG_TRACE(__FUNCTION__ ": Assertion '" #COND "' failed!\n"); \
                              }

#define DBG_ASSERT(COND) if ((COND) == false) { \
                            DBG_TRACE(__FUNCTION__ ": Assertion '" #COND "' failed!\n"); \
                            handle_assert(__FUNCTION__, #COND); \
                         }

#define DBG_FAIL(MSG) DBG_TRACE(__FUNCTION__ MSG "\n"); \
                      fail(__FUNCTION__, MSG);


    inline 
    void trace(const char* msg, ...)
    {
        char buff[1024];

        va_list args;
        va_start(args, msg);
        vsnprintf(buff, 1024, msg, args);

        OutputDebugStringA(buff);

        va_end(args);
    }

    inline
    std::string basename(const std::string& file)
    {
        unsigned int i = file.find_last_of("\\/");
        if (i == std::string::npos)
        {
            return file;
        }
        else
        {
            return file.substr(i + 1);
        }
    }

    std::vector<StackFrame> stack_trace()
    {
        #if _WIN64
        DWORD machine = IMAGE_FILE_MACHINE_AMD64;
        #else
        DWORD machine = IMAGE_FILE_MACHINE_I386;
        #endif
        HANDLE process = GetCurrentProcess();
        HANDLE thread  = GetCurrentThread();
                
        if (SymInitialize(process, NULL, TRUE) == FALSE)
        {
			std::string msg = std::string(__FUNCTION__) + std::string(": Failed to call SymInitialize.");
            DBG_TRACE(msg.c_str());
            return std::vector<StackFrame>(); 
        }

        SymSetOptions(SYMOPT_LOAD_LINES);
        
        CONTEXT    context = {};
        context.ContextFlags = CONTEXT_FULL;
        RtlCaptureContext(&context);

        #if _WIN64
        STACKFRAME frame = {};
        frame.AddrPC.Offset = context.Rip;
        frame.AddrPC.Mode = AddrModeFlat;
        frame.AddrFrame.Offset = context.Rbp;
        frame.AddrFrame.Mode = AddrModeFlat;
        frame.AddrStack.Offset = context.Rsp;
        frame.AddrStack.Mode = AddrModeFlat;
        #else
        STACKFRAME frame = {};
        frame.AddrPC.Offset = context.Eip;
        frame.AddrPC.Mode = AddrModeFlat;
        frame.AddrFrame.Offset = context.Ebp;
        frame.AddrFrame.Mode = AddrModeFlat;
        frame.AddrStack.Offset = context.Esp;
        frame.AddrStack.Mode = AddrModeFlat;
        #endif

       
        bool first = true;

        std::vector<StackFrame> frames;
        while (StackWalk(machine, process, thread, &frame, &context , NULL, SymFunctionTableAccess, SymGetModuleBase, NULL))
        {
            StackFrame f = {};
            f.address = frame.AddrPC.Offset;
            
            #if _WIN64
            DWORD64 moduleBase = 0;
            #else
            DWORD moduleBase = 0;
            #endif

            moduleBase = SymGetModuleBase(process, frame.AddrPC.Offset);

            char moduelBuff[MAX_PATH];            
            if (moduleBase && GetModuleFileNameA((HINSTANCE)moduleBase, moduelBuff, MAX_PATH))
            {
                f.module = basename(moduelBuff);
            }
            else
            {
                f.module = "Unknown Module";
            }
            #if _WIN64
            DWORD64 offset = 0;
            #else
            DWORD offset = 0;
            #endif
            char symbolBuffer[sizeof(IMAGEHLP_SYMBOL) + 255];
            PIMAGEHLP_SYMBOL symbol = (PIMAGEHLP_SYMBOL)symbolBuffer;
            symbol->SizeOfStruct = (sizeof(IMAGEHLP_SYMBOL)) + 255;
            symbol->MaxNameLength = 254;

            if (SymGetSymFromAddr(process, frame.AddrPC.Offset, &offset, symbol))
            {
                f.name = symbol->Name;
            }
            else
            {
                DWORD error = GetLastError();
				std::string msg = std::string(__FUNCTION__) + std::string(": Failed to resolve address 0x%X: %u\n");
                DBG_TRACE(msg.c_str(), frame.AddrPC.Offset, error);
                f.name = "Unknown Function";
            }
            
            IMAGEHLP_LINE line;
            line.SizeOfStruct = sizeof(IMAGEHLP_LINE);
            
            DWORD offset_ln = 0;
            if (SymGetLineFromAddr(process, frame.AddrPC.Offset, &offset_ln, &line))
            {
                f.file = line.FileName;
                f.line = line.LineNumber;
            }
            else
            {
                DWORD error = GetLastError();
				std::string msg = std::string(__FUNCTION__) + std::string(": Failed to resolve line for 0x%X: %u\n");
                DBG_TRACE(msg.c_str(), frame.AddrPC.Offset, error);
                f.line = 0;
            } 

            if (!first)
            { 
                frames.push_back(f);
            }
            first = false;
        }

        SymCleanup(process);

        return frames;
    }
    
    inline 
    void handle_assert(const char* func, const char* cond)
    {
        std::stringstream buff;
        buff << func << ": Assertion '" << cond << "' failed! \n";
        buff << "\n";
        
        std::vector<StackFrame> stack = stack_trace();
        buff << "Callstack: \n";
        for (unsigned int i = 0; i < stack.size(); i++)
        {
            buff << "0x" << std::hex << stack[i].address << ": " << stack[i].name << "(" << std::dec << stack[i].line << ") in " << stack[i].module << "\n";
        }

        MessageBoxA(NULL, buff.str().c_str(), "Assert Failed", MB_OK|MB_ICONSTOP);
        abort();
    }

    inline 
    void fail(const char* func, const char* msg)
    {
        std::stringstream buff;
        buff << func << ":  General Software Fault: '" << msg << "'! \n";
        buff << "\n";
        
        std::vector<StackFrame> stack = stack_trace();
        buff << "Callstack: \n";
        for (unsigned int i = 0; i < stack.size(); i++)
        {
            buff << "0x" << std::hex << stack[i].address << ": " << stack[i].name << "(" << stack[i].line << ") in " << stack[i].module << "\n";
        }

        MessageBoxA(NULL, buff.str().c_str(), "General Software Fault", MB_OK|MB_ICONSTOP);
        abort();
    }
} // namespace dbg
#endif 

}  // namespace tools
