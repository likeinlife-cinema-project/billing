#!/bin/sh

python manage.py collectstatic --noinput
while ! nc -z $PG_ADMIN_BILLING_HOST $PG_ADMIN_BILLING_PORT; do
      sleep 3
done

python manage.py migrate
python manage.py createsuperuser --noinput

if [ "$DJANGO_ADMIN_BILLING_DEBUG" = "True" ]; then
      echo "DEBUG MODE"
      python manage.py runserver 0.0.0.0:$1
else
      echo "RELEASE MODE"
      uwsgi --strict --ini uwsgi.ini
fi