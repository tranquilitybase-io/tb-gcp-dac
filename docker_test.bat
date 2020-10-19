docker build -t gcr.io/tranquility-base-images/tb-gcp-dac:local .
REM docker-compose -f docker-compose-local.yml up --scale worker=3
docker-compose -f docker-compose-local.yml up