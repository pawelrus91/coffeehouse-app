from typing import TypedDict, Unpack

import factory
from factory.faker import faker

from apps.auth.models import User


class UserCredentials(TypedDict):
    email: str
    password: str


class RegistrationUser(UserCredentials):
    password_confirm: str


class RegistrationFactory(factory.Factory):
    email = factory.Faker('ascii_safe_email')
    password = factory.Faker('password')

    @factory.lazy_attribute
    def password_confirm(self):
        return self.password

    @classmethod
    def payload(cls, **kwargs: Unpack[RegistrationUser]) -> RegistrationUser:
        return factory.build(dict, FACTORY_CLASS=cls, **kwargs)


class UserFactory(factory.django.DjangoModelFactory[User]):
    class Meta:
        model = User

    email = factory.Faker('ascii_safe_email')
    password = factory.django.Password('secret')

    @classmethod
    def credentials(cls, **kwargs: Unpack[UserCredentials]) -> UserCredentials:
        fake = faker.Faker()
        return {
            'email': fake.ascii_safe_email(),
            'password': fake.password(),
            **kwargs,
        }
