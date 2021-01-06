#!/bin/bash
cd ../../../

# variables
image_name=gcr.io/tranquility-base-images/tb-gcp-dac:main

# Run unit tests
python3 -m unittest discover -s src/test/python/tranquilitybase/gcpdac/unit/

# Build
docker build \
  -t $image_name \
  -f build_src/gcpdac/main/Dockerfile \
  --build-arg python_src=src/main/python/tranquilitybase/gcpdac_mock \
 .

# Spin up
docker-compose -f build_src/gcpdac/mock/docker-compose.yml up
