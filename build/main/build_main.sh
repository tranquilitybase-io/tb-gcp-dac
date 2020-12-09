#!/bin/bash
cd ../../
image_name=gcr.io/tranquility-base-images/tb-gcp-dac:main

docker build \
  -t $image_name \
  -f build/main/Dockerfile \
 .

id=$(docker images --filter="reference=${image_name}" --quiet)
#docker run $id python3 -m unittest discover -s src/test/python/tranquilitybase/gcpdac/unit/
