FROM python:3.11-alpine

RUN apk add bash

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apk add postgresql-dev build-base postgresql-client

WORKDIR ./main

RUN mkdir /main/static && mkdir /main/media

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD []