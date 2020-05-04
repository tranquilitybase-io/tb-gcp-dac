#!/bin/sh
LOGLEVEL=debug

gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS"

celery -A celery_worker worker --log-level="${LOGLEVEL}"
