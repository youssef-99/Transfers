FROM python:3.11-slim

LABEL maintainer="Youssef William"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app

RUN apt-get update && \
    python3 -m venv --system-site-packages /py && \
    /py/bin/pip3 install --upgrade pip && \
    /py/bin/pip3 install -r /requirements.txt

ENV PATH="/scripts:/py/bin:$PATH"

COPY . .
