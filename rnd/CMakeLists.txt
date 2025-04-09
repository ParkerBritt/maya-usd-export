cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME helloWorld)
set(MAYA_LOCATION "/usr/autodesk/maya2023")
set(MAYA_USD_LOCATION "/usr/autodesk/mayausd/maya2023/0.20.0_202211021008-b68700b/mayausd")
# set(MAYA_USD_LIB_LOCATION "${MAYA_USD_LOCATION}")
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
    # "${USD_LOCATION}/include"
    "${MAYA_USD_LOCATION}/MayaUSD/include"
    $ENV{DEVKIT_LOCATION}/devkit/ufe/include
)

add_definitions(-std=c++17)

build_plugin()


file(GLOB USD_LIBS "${MAYA_USD_LOCATION}/USD/lib/*.so")

target_link_libraries(${PROJECT_NAME}
    # "${USD_LOCATION}/lib/libusd_usd.so"
    # "${USD_LOCATION}/lib/libusd_usdGeom.so"
    # "${USD_LOCATION}/lib/libusd_vt.so"

    # "${MAYA_USD_LOCATION}/USD/lib/libusd.so"
    # "${MAYA_USD_LOCATION}/USD/lib/libusdGeom.so"
    # "${MAYA_USD_LOCATION}/USD/lib/libkind.so"
    # "${MAYA_USD_LOCATION}/USD/lib/libpcp.so"
    # "${MAYA_USD_LOCATION}/USD/lib/libsdf.so"
    ${USD_LIBS}

    "${MAYA_USD_LOCATION}/MayaUSD/lib/libmayaUsd.so"
    "${MAYA_USD_LOCATION}/MayaUSD/lib/libmayaUsdUtils.so"
    
)
