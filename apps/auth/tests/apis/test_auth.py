import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.auth.tests.factories import RegistrationFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


def get_register_url():
    return reverse('auth:register')


@pytest.mark.django_db
def test_that_property_create_user_model_on_register_endpoint(api_client):
    valid_payload = RegistrationFactory.payload()

    request = api_client.post(get_register_url(), data=valid_payload)
    user = User.objects.filter(email=valid_payload['email'])

    assert request.status_code == status.HTTP_201_CREATED
    assert request.json() == {
        'message': 'User was successfully registered.',
    }
    assert user.exists()


@pytest.mark.django_db
def test_when_password_and_password_confirm_is_different_then_400(api_client):
    invalid_payload = RegistrationFactory.payload(
        password='secret',
        password_confirm='different_secret',
    )
    request = api_client.post(get_register_url(), data=invalid_payload)

    assert request.status_code == status.HTTP_400_BAD_REQUEST
    assert request.json() == {
        'password': ['The password and confirmation password must match.'],
    }


@pytest.mark.django_db
def test_when_email_address_exists_in_database_then_400(api_client):
    valid_payload = RegistrationFactory.payload()
    User.objects.create_user(
        email=valid_payload['email'],
        password=valid_payload['password'],
    )

    request = api_client.post(get_register_url(), data=valid_payload)

    assert request.status_code == status.HTTP_400_BAD_REQUEST
    assert request.json() == {
        'email': ['user with this email address already exists.'],
    }
