#!/bin/bash
cd ../../

image_name=gcr.io/tranquility-base-images/tb-gcp-dac:unit_test

docker build \
  -t $image_name \
  -f src/main/docker/Dockerfile_test \
 .

id=$(docker images --filter="reference=${image_name}" --quiet)
docker run $id python3 -m unittest discover -s src/test/gcpdac_tests/unit/