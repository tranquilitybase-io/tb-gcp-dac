#!/bin/sh
LOGLEVEL=debug
NUMBER_OF_WORKERS=1
PORT=3100

if [ ! -z "${1}" ]; then
	PORT=${1}
fi
echo "Using port: ${PORT}"
FLASK_RUN_PORT=${PORT}

# credentials must be added as a volume for this to work - TODO tackle better?
# docker called like this - `docker run -p 3100:3100 gcr.io/tranquility-base-images/tb-gcp-dac:alpha -v <EC CONFIG YAML FILE>:/ec-config.yaml:ro -v <CREDENTIALS FILE>:/credentials.json:ro -e GOOGLE_CLOUD_PROJECT=<GOOGLE PROJECT ID> -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json`

gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"
# TODO do this from within app?
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

DEBUG="True" gunicorn --workers=${NUMBER_OF_WORKERS} --bind=0.0.0.0:${PORT} --log-level="${LOGLEVEL}" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' app:connex_app
