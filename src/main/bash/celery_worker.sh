#!/bin/sh
LOGLEVEL=debug
celery -A celery_worker worker --concurrency=5 --task-events  --loglevel="${LOGLEVEL}"