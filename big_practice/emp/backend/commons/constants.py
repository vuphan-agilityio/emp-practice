from django.conf import settings

"""Errors code constants."""
ERRORS_CODE = {
    'UNAUTHORIZED': {
        'code': 401,
        'message': 'Authorization failed with the provided credentials.'
    },
    'DOES_NOT_EXITS': {
        'code': 401,
        'message': 'The {obj} does exits in system.'
    },
    'MISSING_FIELD': {
        'code': 402,
        'message': 'Must provide field ``{field}`` when creating a {obj}.'
    },
    'DUPLICATE_VALUE': {
        'code': 403,
        'message': 'This {obj} is already exits. Please enter another one.'
    },
    'INVALID_PAGE': {
        'code': 404,
        'message': 'Sorry, no results on that page.'
    },
    'EMAIL_FAILED': {
        'code': 405,
        'message': 'Cannot send email.'
    },
    'INVALID_DATA': {
        'code': 406,
        'message': 'Data is not valid.'
    },
    'UNKNOWNERROR': {
        'code': 407,
        'message': 'Unknown error.'
    },
    'INVALID_OPERATOR': {
        'code': 408,
        'message': 'Client performed a invalid operation'
    },
    'UNLOGIN': {
        'code': 409,
        'message': 'Please login again.'
    },
    'MISSING_PARAMATER': {
        'code': 410,
        'message': 'Missing requred paramaters'
    },
    'ACCOUNT_EXIST': {
        'code': 411,
        'message': 'Account exist!'
    },
    'DATABASE_ERROR': {
        'code': 412,
        'message': 'Database have something error!'
    },
    'PERMISSION_ERROR': {
        'code': 413,
        'message': 'Permission denied!'
    }
}

"""JWT constants."""
JWT_AUTH = {
    'JWT_SECRET': settings.SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXP_DELTA_SECONDS': 108000
}
