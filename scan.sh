#!/bin/bash

function verify_exit_code
{
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo "$1" 1>&2
    exit $exit_code
  fi
}

source ../env/bin/activate

pip install pep8==1.5.6
verify_exit_code "Failed to install pep8 package"

pep8 --ignore=E501 ./
verify_exit_code "There are pep8 errors"

pip install -e ./
verify_exit_code "There are install errors"

python ./run_tests.py
verify_exit_code "There are issues with steps usage"