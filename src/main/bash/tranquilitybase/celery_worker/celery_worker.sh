#!/bin/sh
LOGLEVEL=debug

# unresolved problems with celery path resolution and import mechanics
# not readily able to redirect the paths

#python -c "import src/main/python/tranquilitybase/"
celery -A celery_worker worker \
 --concurrency=5 \
 --task-events \
 --loglevel="${LOGLEVEL}"
# --workdir src/main/python/tranquilitybase/celery_worker