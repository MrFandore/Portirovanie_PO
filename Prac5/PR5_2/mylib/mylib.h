#ifndef MYLIB_H
#define MYLIB_H

#ifdef _WIN32
  #ifdef MYLIB_EXPORTS
    #define MYLIB_API __declspec(dllexport)
  #else
    #define MYLIB_API __declspec(dllimport)
  #endif
#else
  #define MYLIB_API
#endif

// Простая функция
MYLIB_API int add(int a, int b);

// Более сложная функция
MYLIB_API void print_message(const char* msg);

#endif