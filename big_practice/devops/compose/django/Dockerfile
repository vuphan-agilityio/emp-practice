# --- Base Python ---
FROM python:3.6-alpine AS base

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

RUN apk add --no-cache --virtual .build-deps \
                                ca-certificates \
                                gcc \
                                postgresql-dev \
                                linux-headers \
                                musl-dev \
                                libffi-dev \
                                jpeg-dev zlib-dev \
                                bash

COPY . /code

# ------------------------------
# --- Stage DEV DEPENDENCIES ---
FROM base as dev-dependencies

# Requirements local have to be pulled and installed here, otherwise caching won't work
COPY ./devops/requirements /code/requirements
RUN pip install -r /code/requirements/local.txt
COPY . /local-dependencies

# ------------------------------
# --- Stage DEV DEPENDENCIES ---
FROM base as prod-dependencies

# Requirements prod have to be pulled and installed here, otherwise caching won't work
COPY ./devops/requirements /code/requirements
RUN pip install -r /code/requirements/production.txt
COPY . /prod-dependencies

# -------------------------
# --- Stage DEVELOPMENT ---
FROM dev-dependencies AS dev

# Execute entrypoint to get postgres user and password
COPY ./devops/compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy script runserver django
COPY ./devops/compose/django/runserver.sh /runserver.sh
RUN chmod +x /runserver.sh

WORKDIR /code
WORKDIR /dev-dependencies
ENTRYPOINT [ "/entrypoint.sh" ]

# ------------------------
# --- Stage PRODUCTION ---
FROM prod-dependencies AS prod

# Allow executing gunicorn script
COPY ./devops/compose/django/gunicorn.sh /gunicorn.sh
RUN chmod +x /gunicorn.sh

# Allow executing entrypoint to get postgres user and password
COPY ./devops/compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy script runserver django
COPY ./devops/compose/django/runserver.sh /runserver.sh
RUN chmod +x /runserver.sh

WORKDIR /code
WORKDIR /prod-dependencies
ENTRYPOINT [ "/entrypoint.sh" ]
