CXX = g++
CXXFLAGS = -Wall -std=c++11 -I.

# Динамическая библиотека
shared: mylib/mylib.cpp
	$(CXX) -fPIC -shared -DMYLIB_EXPORTS $< -o libmylib.so

# Статическая библиотека
static: mylib/mylib.cpp
	$(CXX) -c $< -o mylib.o
	ar rcs libmylib.a mylib.o

# Статическая линковка программы
main-static: main.cpp static
	$(CXX) $< libmylib.a -o main_static

# Динамическая линковка программы
main-shared: main.cpp shared
	$(CXX) $< -L. -lmylib -o main_shared

clean:
	rm -f *.o *.a *.so main_*