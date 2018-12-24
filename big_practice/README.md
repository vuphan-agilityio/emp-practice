# API application for big practice

## DevOps

### Docker

An open platform for distributed applications for developers and sysadmins

[Homepage](https://www.docker.com/)

## Backend Frameworks

### Django

Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

[Homepage](https://www.djangoproject.com/)

### Tastypie

Tastypie is a web service API framework for Django. It provides a convenient, yet powerful and highly customizable, abstraction for creating REST-style interfaces.

## Databases

### PostgreSQL

PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness.

[Homepage](http://www.postgresql.org/)

### Psycopg

Psycopg is the most popular PostgreSQL adapter for the Python programming language. At its core it fully implements the Python DB API 2.0 specifications. Several extensions allow access to many of the features offered by PostgreSQL.

[Homepage](http://initd.org/psycopg/)

## Web Servers

### nginx

Nginx (pronounced "engine-ex") is an open source reverse proxy server for HTTP, HTTPS, SMTP, POP3, and IMAP protocols, as well as a load balancer, HTTP cache, and a web server (origin server). The nginx project started with a strong focus on high concurrency, high performance and low memory usage. It is licensed under the 2-clause BSD-like license and it runs on Linux, BSD variants, Mac OS X, Solaris, AIX, HP-UX, as well as on other *nix flavors.

[Homepage](http://nginx.org/)

### Gunicorn

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

[Homepage](http://gunicorn.org/)

### PyJWT

A Python implementation of RFC 7519. Original implementation was written by @progrium.

[Homepage](https://pyjwt.readthedocs.io/en/latest/index.html)

## Usage

Develop on local machine:

*Required installed virtualenv and virtualenvwrapper*

Create virtual enviroment:

- `$ cd my_project_folder`
- `$ mkvirtualenv venv`

Active enviroment: `$ workon venv`

Install package: `$ pip install -r requirements/local.txt`

Create DB:

- `$ sudo su postgres`
- `$ psql`
- `CREATE DATABASE python-training;`

Maybe you need to create new user: `CREATE USER dev WITH PASSWORD 'dev_password';`

========>DONE

makemigrations, migrate, createsuperuser and runserver.
