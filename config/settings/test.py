from config.settings.base import *  # noqa

# Speeding up the tests
# https://docs.djangoproject.com/en/6.1/topics/testing/overview/#speeding-up-the-tests

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
