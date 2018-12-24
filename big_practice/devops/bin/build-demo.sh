#!/usr/bin/env bash
docker build -t emp-django/app-api:demo ../compose/django
docker build -t emp-postgres/app-api:demo ../compose/postgres
docker build -t emp-nginx/app-api:demo ../compose/nginx
