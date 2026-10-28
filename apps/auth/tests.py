import datetime
import uuid

import pytest
from django.contrib.auth import get_user_model
from django.db import models

from apps.auth.models import User


def test_that_user_model_exists():
    assert issubclass(User, models.Model)


@pytest.mark.django_db
def test_that_user_model_is_created_with_minimum_inputs():
    valid_payload = {
        'email': 'user@example.com',
        'password': 'secret',
    }
    user = User(**valid_payload)
    user.full_clean()
    user.save()

    assert user.pk.version == 4
    assert isinstance(user.pk, uuid.UUID)
    assert user.email == valid_payload['email']
    # This field is hashed by the create_user() and create_superuser() methods.
    assert user.password == valid_payload['password']
    assert user.first_name == ''
    assert user.last_name == ''
    assert user.is_active is False
    assert user.is_staff is False
    # assert user.is_superadmin is False
    assert isinstance(user.created_at, datetime.datetime)
    assert isinstance(user.updated_at, datetime.datetime)
    # Test for fields are from django.contrib.auth.model.PermissionsMixin
    assert user.is_superuser is False
    assert User._meta.get_field('groups').many_to_many
    assert User._meta.get_field('user_permissions').many_to_many


def test_that_user_model_is_configured_as_auth_user_model():
    assert User is get_user_model()


@pytest.mark.django_db
def test_that_user_model_formats_its_string_representation():
    user1 = User.objects.create(email='user1@example.com')
    user2 = User.objects.create(
        email='user2@example.com',
        first_name='John',
        last_name='Doe',
    )

    assert str(user1) == '<user1@example.com>'
    assert str(user2) == 'John Doe <user2@example.com>'


@pytest.mark.django_db
def test_that_create_user_raises_error_when_email_is_missing():
    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_user(email=None, password='secret')


@pytest.mark.parametrize(
    ('email', 'normalized_email'),
    [
        ('test1@EXAMPLE.com', 'test1@example.com'),
        ('Test2@Example.com', 'Test2@example.com'),
        ('TEST3@EXAMPLE.com', 'TEST3@example.com'),
        ('test4@example.COM', 'test4@example.com'),
    ],
)
@pytest.mark.django_db
def test_that_create_user_normalizes_email_when_email_contains_mixed_case(
    email,
    normalized_email,
):
    user = User.objects.create_user(email=email, password='secret')

    assert user.email == normalized_email


@pytest.mark.django_db
def test_that_create_user_saves_user():
    valid_payload = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'user@example.com',
        'password': 'secret',
    }
    user = User.objects.create_user(**valid_payload)

    assert User.objects.filter(email=valid_payload['email']).exists()
    assert user.pk.version == 4
    assert isinstance(user.pk, uuid.UUID)
    # password should NOT be raw
    assert user.password != valid_payload['password']
    assert User.check_password(user, valid_payload['password'])
    assert user.email == valid_payload['email']
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.is_active is False
    assert user.is_staff is False
    assert isinstance(user.created_at, datetime.datetime)
    assert isinstance(user.updated_at, datetime.datetime)
    # Test for fields are from django.contrib.auth.model.PermissionsMixin
    assert user.is_superuser is False
    assert User._meta.get_field('groups').many_to_many
    assert User._meta.get_field('user_permissions').many_to_many


@pytest.mark.django_db
def test_that_create_superuser_raises_error_when_email_is_missing():
    with pytest.raises(ValueError, match='Users must have an email address'):
        User.objects.create_superuser(email=None, password='secret')


@pytest.mark.parametrize(
    ('email', 'normalized_email'),
    [
        ('test1@EXAMPLE.com', 'test1@example.com'),
        ('Test2@Example.com', 'Test2@example.com'),
        ('TEST3@EXAMPLE.com', 'TEST3@example.com'),
        ('test4@example.COM', 'test4@example.com'),
    ],
)
@pytest.mark.django_db
def test_that_create_superuser_normalizes_email_when_email_contains_mixed_case(
    email,
    normalized_email,
):
    user = User.objects.create_superuser(email=email, password='secret')

    assert user.email == normalized_email


@pytest.mark.django_db
def test_that_create_superuser_saves_user():
    valid_payload = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'user@example.com',
        'password': 'secret',
    }
    user = User.objects.create_superuser(**valid_payload)

    assert User.objects.filter(email=valid_payload['email']).exists()
    assert user.pk.version == 4
    assert isinstance(user.pk, uuid.UUID)
    # password should NOT be raw
    assert user.password != valid_payload['password']
    assert User.check_password(user, valid_payload['password'])
    assert user.email == valid_payload['email']
    assert user.first_name == 'John'
    assert user.last_name == 'Doe'
    assert user.is_active is True
    assert user.is_staff is True
    assert isinstance(user.created_at, datetime.datetime)
    assert isinstance(user.updated_at, datetime.datetime)
    # Test for fields are from django.contrib.auth.model.PermissionsMixin
    assert user.is_superuser is True
    assert User._meta.get_field('groups').many_to_many
    assert User._meta.get_field('user_permissions').many_to_many
