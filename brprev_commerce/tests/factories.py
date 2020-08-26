import decimal
from datetime import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory

from brprev_commerce.database import db
from brprev_commerce.models import Customer, Product, Purchase, User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    login = factory.Faker('name')
    password = factory.Faker('name')


class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Customer
        sqlalchemy_session = db.session

    name = factory.Faker('name')


class PurchaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Purchase
        sqlalchemy_session = db.session

    created = factory.LazyFunction(lambda: datetime.now())
    customer = factory.SubFactory(CustomerFactory)
    _items = []


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = db.session

    description = factory.Faker('sentence', nb_words=2)
    price = decimal.Decimal('1.99')
