#!/bin/bash
cd ../../../

# variables
image_name=gcr.io/tranquility-base-images/tb-gcp-dac-test-harness:main

# Build
docker build \
  -t $image_name \
  -f build_src/gcpdac/test/Dockerfile_test \
 .

## Spin up
docker-compose -f build_src/gcpdac/test/docker-compose-test.yml up --abort-on-container-exit
