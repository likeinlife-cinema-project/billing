#!/bin/sh
celery -A billing worker -B --loglevel="$CELERY_LOG_LEVEL"