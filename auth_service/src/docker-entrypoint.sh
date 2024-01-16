#!/bin/sh

alembic upgrade head
python -m cli service init-service-accounts

if [ "$AUTH_DEBUG" = "True" ]; then
    echo "DEBUG MODE"
    uvicorn auth_app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "RELEASE MODE"
    gunicorn auth_app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --proxy-allow-from nginx
fi