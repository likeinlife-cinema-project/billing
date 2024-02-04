#!/bin/sh

if [ "$NOTIFY_DEBUG" = "True" ]; then
    echo "DEBUG MODE"
    uvicorn main:app --host 0.0.0.0 --port $1 --reload
else
    echo "RELEASE MODE"
    gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$1 --proxy-allow-from nginx
fi