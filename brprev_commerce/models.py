import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, Numeric,
                        String)
from sqlalchemy.orm import relationship

from brprev_commerce.database import db


class User(db.Model):
    __tablename__ = '_user'

    id = Column(Integer, primary_key=True)
    login = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)


class Customer(db.Model):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)


class PurchaseStates(enum.Enum):
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = Column(Integer, primary_key=True)
    state = Column(Enum(PurchaseStates), default=PurchaseStates.OPENED)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship("Customer")
    created = Column(DateTime, default=lambda: datetime.now())
    closed_at = Column(DateTime)
    _items = relationship("PurchaseItem", backref="parent")

    def add_item(self, product_id, quantity):
        new_item = PurchaseItem(product_id=product_id, quantity=quantity)
        self._items.append(new_item)

    @property
    def subtotal(self):
        if not len(self._items):
            return Decimal(0)
        retval = Decimal(0)
        for item in self._items:
            retval += item.subtotal
        return retval

    @property
    def items(self):
        return self._items

    def close(self):
        if self.state == PurchaseStates.CLOSED:
            return
        self.state = PurchaseStates.CLOSED
        self.closed_at = datetime.now()


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    description = Column(String(30), nullable=False)
    price = Column(Numeric(precision=2), nullable=False)


class PurchaseItem(db.Model):
    __tablename__ = 'purchase_item'

    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product")
    quantity = Column(Integer, nullable=False)

    @property
    def subtotal(self):
        return self.product.price * self.quantity
