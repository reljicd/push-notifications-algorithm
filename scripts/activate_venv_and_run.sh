#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No input path supplied"
    exit 1
fi

INPUT_CSV_PATH=$1

rm -rf venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python notifications_processor/main.py --events_csv_path=INPUT_CSV_PATH --print_to_stdout=True
