FROM python:3.10.13-alpine3.17 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

FROM base as final

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./tests ./tests

ENTRYPOINT ["pytest", "./tests"]