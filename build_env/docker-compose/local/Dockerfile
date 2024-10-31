FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./req.txt .
COPY ./app .

RUN apk update \
    && apk add bash \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r req.txt
