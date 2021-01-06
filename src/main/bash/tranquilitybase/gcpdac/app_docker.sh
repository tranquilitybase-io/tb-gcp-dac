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

#
#if [ -d src/main/python/tranquilitybase/gcpdac/ ]
#then
#    printf "This file exists!!! YAYAYAYA. :]"
#    exit 201
#else
#    printf "no file. NO :["
#    exit 202
#fi
#
#exit 10

[ ! -f src/main/python/tranquilitybase/gcpdac/app.py ] && exit 100

{
  gunicorn app:connex_app \
  --chdir src/main/python/tranquilitybase/gcpdac/
} || {
  echo "what"
  exit 20
}