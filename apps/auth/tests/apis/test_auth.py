import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.auth.tests.factories import RegistrationFactory, UserFactory

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


def get_register_url():
    return reverse('auth:register')


def get_login_url():
    return reverse('auth:login')


# ==================================================
# Registration
# ==================================================


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


# ==================================================
# Login
# ==================================================


@pytest.mark.django_db
def test_when_user_not_exists_then_return_400(api_client):
    valid_payload = UserFactory.credentials()
    response = api_client.post(get_login_url(), data=valid_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'error': ['Unable to log in with provided credentials.'],
    }


@pytest.mark.django_db
def test_when_user_exists_and_is_not_active_then_return_400(api_client):
    valid_payload = UserFactory.credentials()
    UserFactory.create(**valid_payload)

    response = api_client.post(get_login_url(), data=valid_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'error': ['Unable to log in with provided credentials.'],
    }


@pytest.mark.django_db
def test_when_user_exists_and_is_active_then_return_tokens(api_client):
    valid_payload = UserFactory.credentials()
    UserFactory.create(is_active=True, **valid_payload)

    response = api_client.post(get_login_url(), data=valid_payload)

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.json()
    assert 'refresh' in response.json()


# ==================================================
# Me
# ==================================================


@pytest.mark.django_db
def test_when_is_unauthenticated_then_return_401(api_client):
    UserFactory.create()

    response = api_client.get(reverse('auth:me'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_when_user_has_token_credentials_then_show_user_details(api_client):
    valid_payload = UserFactory.credentials()
    user = UserFactory.create(is_active=True, **valid_payload)

    tokens_response = api_client.post(get_login_url(), data=valid_payload)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + tokens_response.data['access'])

    response = api_client.get(reverse('auth:me'))

    expected_response = {
        'id': str(user.id),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
