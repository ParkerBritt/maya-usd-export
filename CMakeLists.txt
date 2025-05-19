cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(PROJECT_NAME maya_usd_export)
set(CMAKE_AUTOMOC ON)

project(${PROJECT_NAME})

# options
option(BUILD_TESTS "builds tests" OFF)

# set vars
# set from USD_LOCATION environment variable if exists
if(NOT DEFINED USD_LOCATION AND DEFINED ENV{USD_LOCATION})
    set(USD_LOCATION $ENV{USD_LOCATION} CACHE PATH "Path to USD installation")
else()
    set(USD_LOCATION "/opt/USD" CACHE PATH "Path to USD installation")
endif()

message(STATUS "Setting USD_LOCATION to '${USD_LOCATION}'")
message(STATUS "Setting DEVKIT_LOCATION to '$ENV{DEVKIT_LOCATION}'")
if(NOT DEFINED ENV{DEVKIT_LOCATION})
    message(FATAL_ERROR "$DEVKIT_LOCATION is not set. Please set it as an env var.")
endif()

find_package(Qt5 REQUIRED COMPONENTS Widgets Core)
qt5_add_resources(RESOURCES static/resources.qrc)

# export compile commands for linter
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


# silence warnings
add_compile_options(
# maya devkit warnings
 -Wno-deprecated
 -Wno-redundant-move
 -Wno-missing-field-initializers
 -Wno-deprecated-copy
 -Wno-cast-user-defined

 # silence tbb usd compile issue
 -Wno-changes-meaning
)


# setup core
add_library(maya_usd_export_core STATIC
    src/export/PrimWriter.cpp
    src/export/ExportItem.cpp
)

set_target_properties(maya_usd_export_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(maya_usd_export_core
    PUBLIC "${USD_LOCATION}/include"
    PRIVATE "$ENV{DEVKIT_LOCATION}/include"
    PUBLIC include
    PRIVATE src
)
target_link_libraries(maya_usd_export_core
    "${USD_LOCATION}/lib/libusd_usd.so"
    "${USD_LOCATION}/lib/libusd_usdGeom.so"
    # "${USD_LOCATION}/lib/libusd_vt.so"
)


# setup plugin

# load devkit

set(interface_sources
    src/interface/main_export_dialog.cpp
    src/interface/main_export_dialog.h

    src/interface/controllers/MainExportDialogController.cpp
    src/interface/controllers/SelectionOptionsController.cpp

    src/interface/widgets/CollapsibleContainer.h
    src/interface/widgets/CollapsibleContainer.cpp

    src/interface/widgets/GeneralOptions.h
    src/interface/widgets/GeneralOptions.cpp

    src/interface/widgets/SelectionOptions.h
    src/interface/widgets/SelectionOptions.cpp

    src/interface/widgets/AnimationOptions.h
    src/interface/widgets/AnimationOptions.cpp

    src/interface/widgets/SelectionParameters.h
    src/interface/widgets/SelectionParameters.cpp

    src/interface/models/DAGSelectionModel.cpp
    src/interface/models/DAGSelectionModel.h

)

set(SOURCE_FILES
    src/plugin_entry.cpp
    ${interface_sources}
    ${RESOURCES}

)
include($ENV{DEVKIT_LOCATION}/cmake/pluginEntry.cmake)

set(
    LIBRARIES
    OpenMaya
    Foundation
    # Qt5Core
    # Qt5Widgets
)
build_plugin()

target_link_libraries(${PROJECT_NAME}
    maya_usd_export_core
    # "$ENV{DEVKIT_LOCATION}/devkit/lib/libQt5Core.so"
    "${USD_LOCATION}/lib/libusd_usd.so"
)

target_include_directories(${PROJECT_NAME}
    # BEFORE becasue maya's tbb is broken so it uses this one
    BEFORE PRIVATE "${USD_LOCATION}/include"
)


add_definitions(-std=c++17)


# ----
# build interface
# ----
# set(CMAKE_PREFIX_PATH "$ENV{DEVKIT_LOCATION}/cmake/qt_5.15.2")
# set(CMAKE_PREFIX_PATH "$ENV{DEVKIT_LOCATION}/devkit")
message(STATUS "QT DIR: ${Qt5_DIR}")
target_include_directories(${PROJECT_NAME}
    PRIVATE "$ENV{DEVKIT_LOCATION}/include"
    PRIVATE src
)

# ----
# build tests
# ----
if(BUILD_TESTS)
    message(STATUS "BUILDING TESTS")
    # try to find catch2 for testing
    find_package(Catch2 3 QUIET)

    # download if not found
    if(NOT Catch2_FOUND)
        message(STATUS "Catch2 not found, using FetchContent to download it")

        include(FetchContent)
        FetchContent_Declare(
            Catch2
            GIT_REPOSITORY https://github.com/catchorg/Catch2.git
            GIT_TAG        v3.8.1
        )
        FetchContent_MakeAvailable(Catch2)
    endif()


    # source tests
    add_executable(tests tests/unit-tests/test-main.cpp)


    # link to core lib

    set(LIBRARY_DIRS $ENV{DEVKIT_LOCATION})
    find_library(OpenMaya_PATH
        NAMES OpenMaya
        PATHS ${LIBRARY_DIRS}
        NO_DEFAULT_PATH
    )
    find_library(Foundation_PATH
        NAMES Foundation
        PATHS ${LIBRARY_DIRS}
        NO_DEFAULT_PATH
    )

    message(STATUS "OPEN MAYA PATH: ${OpenMaya_PATH}")
    message(STATUS "OPEN FOUNDATION PATH: ${Foundation_PATH}")

    target_link_libraries(tests PRIVATE
        Catch2::Catch2WithMain
        maya_usd_export_core
        # ${OpenMaya_PATH}
        # ${Foundation_PATH}
    )

    target_include_directories(tests BEFORE
         PUBLIC "${USD_LOCATION}/include"
    )

    # target_include_directories(tests
    #     PUBLIC "$ENV{DEVKIT_LOCATION}/include"
    # )

    
    # ctest
    include(CTest)
    include(Catch)
    catch_discover_tests(tests)
endif()
