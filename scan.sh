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

pip install nose==1.3.3 pep8==1.6.2 teamcity-messages==1.12
verify_exit_code "Failed to install python packages"

pep8 --ignore=E501 ./
verify_exit_code "There are pep8 errors"

pip install -e ./
verify_exit_code "There are install errors"

python ./run_tests.py
verify_exit_code "There are issues with steps usage"
