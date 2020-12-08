#!/bin/bash

docker build \
  -t gcr.io/tranquility-base-images/tb-gcp-dac:main \
  -f src/main/docker/Dockerfile \
 --build-arg python_src=src/main/python/tranquilitybase/gcpdac_mock \
 .