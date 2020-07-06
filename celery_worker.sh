#!/bin/sh
LOGLEVEL=debug
celery -E -A celery_worker worker --loglevel="${LOGLEVEL}" --concurrency=5