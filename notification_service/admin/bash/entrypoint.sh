#!/bin/bash

python manage.py collectstatic --noinput
while ! nc -z $PG_ADMIN_NF_DB_HOST $PG_ADMIN_NF_DB_PORT; do
      sleep 0.1
done
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_ADMIN_NF_SUPERUSER_USERNAME', '$DJANGO_ADMIN_NF_SUPERUSER_EMAIL', '$DJANGO_ADMIN_NF_SUPERUSER_PASSWORD')" | python3 manage.py shell
uwsgi --strict --ini uwsgi.ini