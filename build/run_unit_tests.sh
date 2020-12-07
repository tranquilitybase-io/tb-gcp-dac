#!/bin/bash
cd ..
export PYTHONPATH=$(pwd)
python3 -m unittest discover src/test/gcpdac_tests/unit

