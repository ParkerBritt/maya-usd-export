#!/usr/bin/env bash

MAYAPY_PATH="/usr/autodesk/maya/bin/mayapy"
if [ ! -e ]; then
    echo "Error: mayapy not found" >&2
    exit 1
fi


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

export PYTHONPATH="$(realpath ${BASE_DIR}/..):$PYTHONPATH"

PIP_LIST=$("${MAYAPY_PATH}" -m pip list 2>/dev/null)
# echo "${PIP_LIST}"
# check pytest is installed
if [ -z "$(echo ${PIP_LIST} | grep pytest)" ]; then
    echo "Error: failed to find pytest" >&2
    exit 1
fi
echo "found pytest"

"${MAYAPY_PATH}" -m pytest "${BASE_DIR}/tests.py"

