#!/usr/bin/env bash
docker-compose -f docker-compose.dev.yml run django python /code/manage.py shell
