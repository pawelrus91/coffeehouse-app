import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_that_property_crete_user_model_on_register_endpoint(api_client):
    valid_payload = {
        'email': 'user@example.com',
        'password': 'secret',
        'password_confirm': 'secret',
    }
    request = api_client.post(reverse_lazy('auth:register'), data=valid_payload)
    user = User.objects.filter(email=valid_payload['email'])

    assert request.status_code == status.HTTP_201_CREATED
    assert request.json() == {
        'message': 'User was successfully registered.',
    }
    assert user.exists()


@pytest.mark.django_db
def test_when_password_and_password_confirm_is_different_then_400(api_client):
    invalid_payload = {
        'email': 'user@example.com',
        'password': 'secret',
        'password_confirm': 'different_secret',
    }
    request = api_client.post(reverse_lazy('auth:register'), data=invalid_payload)

    assert request.status_code == status.HTTP_400_BAD_REQUEST
    assert request.json() == {
        'password': ['The password and confirmation password must match.'],
    }


@pytest.mark.django_db
def test_when_email_address_exists_in_database_then_400(api_client):
    valid_payload = {
        'email': 'user@example.com',
        'password': 'secret',
        'password_confirm': 'secret',
    }
    User.objects.create_user(
        email=valid_payload['email'],
        password=valid_payload['password'],
    )

    request = api_client.post(reverse_lazy('auth:register'), data=valid_payload)

    assert request.status_code == status.HTTP_400_BAD_REQUEST
    assert request.json() == {
        'email': ['user with this email address already exists.'],
    }
