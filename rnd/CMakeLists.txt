cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME helloWorld)
project(${PROJECT_NAME})

# silence warnings
add_compile_options(
 -Wno-deprecated
 -Wno-redundant-move
 -Wno-missing-field-initializers
 -Wno-deprecated-copy
 -Wno-cast-user-defined
)

include(
    $ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake
)

set(SOURCE_FILES
    helloWorld.cpp
)

set(
    LIBRARIES
    OpenMaya
    Foundation
)

include_directories(
    "/home/parker/Downloads/usd-build/include"
    "/usr/autodesk/mayausd/maya2024/0.25.0_202310160731-bbc8cc8/mayausd/MayaUSD/include"
    $ENV{DEVKIT_LOCATION}/devkit/ufe/include
)

add_definitions(-std=c++17)

build_plugin()

target_link_libraries(${PROJECT_NAME}
    "/home/parker/Downloads/usd-build/lib/libusd_usd.so"
    "/home/parker/Downloads/usd-build/lib/libusd_usdGeom.so"
)
