import factory
from factory.django import DjangoModelFactory
from faker import Factory

from auth_.models import Auth

__all__ = ["AuthFactory"]

fake = Factory.create()


class AuthFactory(DjangoModelFactory):
    class Meta:
        model = Auth

    password = fake.password()
    email = factory.LazyAttribute(fake.email)
    data = factory.LazyAttribute(lambda u: dict(fullname=u.email.split("@", 1).pop(0)))
