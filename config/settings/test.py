from config.settings.base import *  # noqa
from config.settings.base import REST_FRAMEWORK as BASE_REST_FRAMEWORK

# Speeding up the tests
# https://docs.djangoproject.com/en/6.1/topics/testing/overview/#speeding-up-the-tests

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]


# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/#api-reference

REST_FRAMEWORK = {
    **BASE_REST_FRAMEWORK,
    'DEFAULT_THROTTLE_CLASSES': [],
}
