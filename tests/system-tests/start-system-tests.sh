#!/usr/bin/env bash

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

echo "$@"
/usr/autodesk/maya/bin/mayapy -m pytest -s "${BASE_DIR}/system-tests.py" "$@"

