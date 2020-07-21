# CMakeList.txt : CMake project for native, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

project ("native")

# Add source to this project's executable.
add_executable (native "native.cpp" "native.h")

# TODO: Add tests and install targets if needed.
