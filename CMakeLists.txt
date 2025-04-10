cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME maya_usd_export)

project(${PROJECT_NAME})

# set vars
set(MAYA_LOCATION "/usr/autodesk/maya" CACHE PATH "Path to maya installation")
set(USD_LOCATION "/opt/USD" CACHE PATH "Path to usd instalation")

message(STATUS "Setting MAYA_LOCATION to '${MAYA_LOCATION}'")
message(STATUS "Setting USD_LOCATION to '${USD_LOCATION}'")

if(NOT DEFINED ENV{DEVKIT_LOCATION})
    message(FATAL_ERROR "$DEVKIT_LOCATION is not set. Please set it as an env var.")
endif()


# export compile commands for linter
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


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
    src/entry.cpp
)

set(
    LIBRARIES
    OpenMaya
    Foundation
)

include_directories(
    "${USD_LOCATION}/include"
    $ENV{DEVKIT_LOCATION}/devkit/ufe/include
    include
)

add_definitions(-std=c++17)

build_plugin()


target_link_libraries(${PROJECT_NAME}
    "${USD_LOCATION}/lib/libusd_usd.so"
    "${USD_LOCATION}/lib/libusd_usdGeom.so"
    # "${USD_LOCATION}/lib/libusd_vt.so"
)
