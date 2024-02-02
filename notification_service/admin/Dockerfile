FROM python:3.10

WORKDIR /opt/admin

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN apt update && apt install -y netcat-traditional

RUN  mkdir -p /var/www/static/ \
     && mkdir -p /var/www/media/ \
     && mkdir -p /opt/admin/static/ \
     && mkdir -p /opt/admin/media/ \
     && pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./bash -R
RUN chmod +x ./docker-entrypoint.sh

ARG PORT=8000
ENV PORT_ENV=${PORT}
EXPOSE $PORT

ARG COMMAND
ENV COMMAND_VAR=${COMMAND}

ENTRYPOINT ./docker-entrypoint.sh $COMMAND_VAR $PORT_ENV