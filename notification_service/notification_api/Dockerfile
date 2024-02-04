FROM python:3.10.13-alpine3.17

WORKDIR /opt/app

RUN apk add curl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./
RUN chmod 777 docker-entrypoint.sh

ARG PORT=8001
ENV APP_PORT=${PORT}
EXPOSE $APP_PORT

ENTRYPOINT ./docker-entrypoint.sh $APP_PORT