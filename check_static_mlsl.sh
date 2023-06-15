#!/bin/bash

WORK_DIR=`dirname "$0"`
# Include the libraries
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}":${WORK_DIR}/lib/z3/bin"
export PYTHONPATH=$PYTHONPATH:"${WORK_DIR}/lib/z3/bin/python"
export PYTHONPATH=$PYTHONPATH:"${WORK_DIR}/lib/waxeye"

if [ "$#" -ne 3 ]; then
    echo 'Illegal number of parameters.'
    echo 'Usage is: check_static_mlsl.sh "python2.7" "formula" "model"'
    exit 1
fi

# The input files
FORMULA="$2"
MODEL="$3"

PYTHON_V27="$1"

${PYTHON_V27} check_static_mlsl.py ${FORMULA} ${MODEL}
