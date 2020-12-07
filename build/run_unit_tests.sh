#!/bin/bash
cd ..
export PYTHONPATH=$(pwd)
cd src/test/gcpdac_tests/unit
python3 -m unittest discover .

