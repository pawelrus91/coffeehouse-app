from typing import TypedDict, Unpack

import factory


class RegistrationUser(TypedDict):
    email: str
    password: str
    password_confirm: str


class RegistrationFactory(factory.Factory):
    email = factory.Faker('email')
    password = factory.Faker('password')

    @factory.lazy_attribute
    def password_confirm(self):
        return self.password

    @classmethod
    def payload(cls, **kwargs: Unpack[RegistrationUser]) -> RegistrationUser:
        return factory.build(dict, FACTORY_CLASS=cls, **kwargs)
