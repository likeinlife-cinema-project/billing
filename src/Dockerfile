FROM python:3.10.13-alpine3.17

WORKDIR /opt/admin

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

RUN apk add netcat-openbsd gcc libc-dev linux-headers

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN     mkdir -p /opt/admin/static/ \
     && mkdir -p /opt/admin/media/ \
     && pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT=8000
ENV PORT_ENV=${PORT}
EXPOSE $PORT

ARG COMMAND
ENV COMMAND_ENV=${COMMAND}

RUN chmod +x ./docker-entrypoint.sh
RUN chmod +x ./bash -R

ENTRYPOINT ./docker-entrypoint.sh $COMMAND_ENV $PORT_ENV
