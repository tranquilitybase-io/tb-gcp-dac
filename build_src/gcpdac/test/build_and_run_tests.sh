#!/bin/bash
cd ../../../

# variables
image_name=gcr.io/tranquility-base-images/tb-gcp-dac-test-harness:main

# Run unit tests
python3 -m unittest discover -s src/test/python/tranquilitybase/gcpdac/unit/

# Build
docker build \
  -t $image_name \
  -f build_src/gcpdac/test/Dockerfile_test \
 .

## Spin up
docker-compose -f build_src/gcpdac/test/docker-compose-test.yml up
