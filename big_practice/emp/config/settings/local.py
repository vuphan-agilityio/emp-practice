# -*- coding: utf-8 -*-
'''
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
'''


from .common import * # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True) # noqa
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default='sd5w_y8ha%fs#%2_h_1z@0y20jez78_^krf4%n--+masllo9q4') # noqa

DATABASES['default'] = env.db("DATABASE_URL") # noqa

TASTYPIE_FULL_DEBUG = True
