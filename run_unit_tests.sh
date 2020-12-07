#!/bin/bash
#cd ..
echo "-------------"
echo $(pwd)
echo "-------------"
ls
echo "-------------"
export PYTHONPATH=$(pwd)
python3 -c "import sys; print(sys.path)"
echo "-------------"

RUN pip install -r src/main/python/tranquilitybase/gcpdac/requirements.txt
python3 -m unittest discover -s src/test/gcpdac_tests/unit/