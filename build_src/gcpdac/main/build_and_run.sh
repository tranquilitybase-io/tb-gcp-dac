#!/bin/bash
cd ../../../

# variables
image_name=gcr.io/tranquility-base-images/tb-gcp-dac:main

# Run unit tests
python3 -m unittest discover -s src/test/python/tranquilitybase/gcpdac/unit/

# Build
docker build_src \
  -t $image_name \
  -f build_src/gcpdac/main/Dockerfile \
 .

# Spin up
docker-compose -f build_src/gcpdac/main/docker-compose.yml up
