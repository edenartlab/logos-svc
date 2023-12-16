# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye AS python

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY src src
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY requirements.lock requirements.txt

RUN apt-get update \
    && apt-get install -y git \
    && pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "src.logos_svc.server:app"]
