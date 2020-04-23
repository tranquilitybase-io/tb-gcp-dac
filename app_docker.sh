#!/bin/sh
LOGLEVEL=debug
NUMBER_OF_WORKERS=1
PORT=3100

if [ ! -z "${1}" ]; then
	PORT=${1}
fi
echo "Using port: ${PORT}"
FLASK_RUN_PORT=${PORT}

gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"

DEBUG="True" gunicorn --workers=${NUMBER_OF_WORKERS} --bind=0.0.0.0:${PORT} --log-level="${LOGLEVEL}" --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' app:connex_app
