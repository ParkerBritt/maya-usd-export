#!/usr/bin/env bash
set -e

echo "SETUP"
export DEVKIT_LOCATION="${HOME}/devkitBase"

# get path of currently running script
SCRIPT_PATH="$(realpath ${BASH_SOURCE})"
echo "script path" $SCRIPT_PATH

# remove script from base path
BASE_DIR="${SCRIPT_PATH%/*}"
echo "base dir: " $BASE_DIR

if [ ! -d "$BASE_DIR" ]; then
    echo "ERROR: BASE DIR NOT FOUND"
    exit
fi

BUILD_DIR="${BASE_DIR}/build"
echo "BUILD DIR " $BUILD_DIR


echo "BUILDING"

CLEAN_BUILD=0
if [ "$CLEAN_BUILD" -eq 1 ] && [ -d "$BUILD_DIR" ]; then
    echo "Existing build dir, deleting now"
    rm -rf $BUILD_DIR
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
    cmake -G Ninja ..
else
    echo "Build dir doesn't exist, creating one now"
    mkdir -p $BUILD_DIR
    cd $BUILD_DIR
    cmake -G Ninja ..
fi

ninja

echo
echo ------------------
echo    Unit Tests
echo ------------------
"${BASE_DIR}/build/tests"

echo
echo ------------------
echo   System Tests
echo ------------------
"${BASE_DIR}/tests/system-tests/start-system-tests.sh"


echo
echo ------------------
echo   Build Success
echo ------------------
