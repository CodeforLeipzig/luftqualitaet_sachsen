from configurations import values


class PostgreSQLDatabases(object):
    """Settings for local PostgreSQL databases."""
    DATABASES = values.DictValue({
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'luftqualitaet_sachsen',
            'USER': 'luftqualitaet_sachsen',
            'PASSWORD': 'luftqualitaet_sachsen',
            'HOST': 'localhost',
        },
    })


class EmptyDatabases(object):
    """Empty databases settings, used to force to overwrite them."""
    DATABASES = values.DictValue({
        'default': {
            'ENGINE': '',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
        },
    })