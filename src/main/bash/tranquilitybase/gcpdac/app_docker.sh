#!/bin/sh
LOGLEVEL=debug
NUMBER_OF_WORKERS=1
PORT=3100



if [ ! -z "${1}" ]; then
  PORT=${1}
fi
echo "Using port: ${PORT}"

#gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"

log_dir='/var/log/tb-gcp-dac.log'
APP_PORT="${PORT}"


if [ -d src/main/python/tranquilitybase/gcpdac/ ]
then
    printf "This file exists!!! YAYAYAYA. :]"
    exit 201
else
    printf "no file. NO :["
    exit 202
fi

exit 10
{
  gunicorn app:connex_app \
  --workers="${NUMBER_OF_WORKERS}" \
  --bind="0.0.0.0:${PORT}" \
  --log-level="${LOGLEVEL}" \
  --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
  --chdir src/main/python/tranquilitybase/gcpdac/
} || {
  echo "what"
  exit 20
}