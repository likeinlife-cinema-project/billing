#!/bin/sh

if [ "$1" = "admin" ]; then
  ./bash/start_admin.sh $2
elif [ "$1" = "celery" ]; then
  ./bash/start_celery.sh
elif [ "$1" = "flower" ]; then
  ./bash/start_flower.sh
else
  echo "Unknown command argument: $1"
fi