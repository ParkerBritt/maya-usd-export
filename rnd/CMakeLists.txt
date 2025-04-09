cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME helloWorld)
set(MAYA_LOCATION "/usr/autodesk/maya2023")
set(USD_LOCATION "/transfer/Parker/usd-build")

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
    "${USD_LOCATION}/include"
    $ENV{DEVKIT_LOCATION}/devkit/ufe/include
)

add_definitions(-std=c++17)

build_plugin()


target_link_libraries(${PROJECT_NAME}
    "${USD_LOCATION}/lib/libusd_usd.so"
    "${USD_LOCATION}/lib/libusd_usdGeom.so"
    # "${USD_LOCATION}/lib/libusd_vt.so"
)
