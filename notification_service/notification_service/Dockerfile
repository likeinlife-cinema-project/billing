FROM python:3.10.13-alpine3.17

ARG CONTAINER_USER="python"
ARG CONTAINER_UID="1000"

RUN adduser -u ${CONTAINER_UID} -s /bin/bash ${CONTAINER_USER} -D

WORKDIR /home/${CONTAINER_USER}/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY src src
COPY docker-entrypoint.sh docker-entrypoint.sh

RUN chmod -R 777 src

USER ${CONTAINER_USER}

ARG COMMAND
ENV COMMAND_VAR=${COMMAND}

ENTRYPOINT ./docker-entrypoint.sh $COMMAND_VAR
