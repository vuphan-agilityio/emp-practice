#!/usr/bin/env bash
docker build -t emp-django/app-api:develop ../compose/django
docker build -t emp-postgres/app-api:develop ../compose/postgres
docker build -t emp-nginx/app-api:develop ../compose/nginx
