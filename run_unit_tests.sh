#!/bin/bash
#cd ..
echo "-------------"
echo $(pwd)
echo "-------------"
ls
echo "-------------"
set-env name=PYTHONPATH::$(pwd)
python3 -c "import sys; print(sys.path)"
python3 -m unittest discover -s src/test/gcpdac_tests/unit/