cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME maya_usd_export)

project(${PROJECT_NAME})

# options
option(BUILD_TESTS "builds tests" ON)

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


# setup core
add_library(maya_usd_export_core STATIC
    src/export/export.cpp
)

set_target_properties(maya_usd_export_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(maya_usd_export_core
    BEFORE PUBLIC "${USD_LOCATION}/include"
    PUBLIC $ENV{DEVKIT_LOCATION}/devkit/ufe/include
    PUBLIC include
)
target_link_libraries(maya_usd_export_core
    "${USD_LOCATION}/lib/libusd_usd.so"
    "${USD_LOCATION}/lib/libusd_usdGeom.so"
    # "${USD_LOCATION}/lib/libusd_vt.so"
)


# setup plugin

# load devkit

set(SOURCE_FILES
    src/entry.cpp
)
include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)

set(
    LIBRARIES
    OpenMaya
    Foundation
)
build_plugin()

target_link_libraries(${PROJECT_NAME}
    maya_usd_export_core
    "${USD_LOCATION}/lib/libusd_usd.so"
)

target_include_directories(${PROJECT_NAME}
    # BEFORE becasue maya's tbb is broken so it uses this one
    BEFORE PRIVATE "${USD_LOCATION}/include"
    PRIVATE $ENV{DEVKIT_LOCATION}/devkit/ufe/include
)


add_definitions(-std=c++17)




if(BUILD_TESTS)
    message(STATUS "BUILDING TESTS")
    find_package(Catch2 3 REQUIRED)

    add_executable(tests tests/unit-tests/test-main.cpp)
    target_link_libraries(tests PRIVATE Catch2::Catch2WithMain maya_usd_export_core)

    target_include_directories(tests
        BEFORE PUBLIC "${USD_LOCATION}/include"
    )


    
    # ctest
    include(CTest)
    include(Catch)
    catch_discover_tests(tests)
endif()
