#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No input parameters supplied"
    exit 1
fi

rm -rf venv

python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

export PYTHONPATH=$PYTHONPATH:$(pwd)

python $@
