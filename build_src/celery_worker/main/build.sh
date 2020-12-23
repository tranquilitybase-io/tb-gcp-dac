#!/bin/bash
cd ../../../

# variables
image_name=gcr.io/tranquility-base-images/tb-gcp-dac-worker:main

# Run unit tests
#python3 -m unittest discover -s src/test/python/tranquilitybase/gcpdac/unit/

# Build
docker build \
  -t $image_name \
  -f build_src/celery_worker/main/Dockerfile \
 .

# Spin up
# docker-compose -f build_src/celery_worker/main/docker-compose.yml up
