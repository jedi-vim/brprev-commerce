from marshmallow import Schema as maSchema
from marshmallow import ValidationError, post_load, validate, validates
from marshmallow_jsonapi import Schema, fields
from sqlalchemy.orm.exc import NoResultFound

from brprev_commerce.database import db
from brprev_commerce.models import Customer, Product, Purchase, User


class UserSchema(Schema):
    id = fields.String(required=True, dump_only=True)
    login = fields.String(required=True, validate=validate.NoneOf(['']))
    password = fields.String(required=True, validate=validate.NoneOf(['']),
                             load_only=True)

    class Meta:
        type_ = 'user'

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)


class CustomerSchema(Schema):
    id = fields.String(required=True, dump_only=True)
    name = fields.String(required=True, validate=validate.NoneOf(['']))

    class Meta:
        type_ = 'customer'

    @post_load
    def create_customer(self, data, **kwargs):
        return Customer(**data)


class PurchaseItemSchema(maSchema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    subtotal = fields.Decimal(places=2, as_string=True, dump_only=True)

    @validates("product_id")
    def validate_product_id(self, value):
        try:
            db.session.query(Product).filter(Product.id == value).one()
        except NoResultFound:
            raise ValidationError(f'Product ID={value} not found')


class PurchaseSchema(Schema):
    id = fields.String(required=True)
    customer_id = fields.Integer(required=True)
    subtotal = fields.Decimal(places=2, as_string=True, required=True,
                              dump_only=True)
    items = fields.Nested(PurchaseItemSchema, many=True, dump_to="_items")
    created = fields.DateTime()
    closed_at = fields.DateTime()
    state = fields.String()

    class Meta:
        type_ = 'purchase'

    @validates("customer_id")
    def validate_customer_id(self, value):
        try:
            db.session.query(Customer).filter(Customer.id == value).one()
        except NoResultFound:
            raise ValidationError(f'Customer ID={value} not found')

    @validates('id')
    def validate_purchase_id(self, value):
        try:
            db.session.query(Purchase).filter(Purchase.id == value).one()
        except NoResultFound:
            raise ValidationError(f'Purchase ID={value} not found')


class ProductSchema(Schema):
    id = fields.String(dump_only=True)
    price = fields.Decimal(places=2, as_string=True, required=True)
    description = fields.String(required=True, validate=validate.NoneOf(['']))

    class Meta:
        type_ = 'product'

    @post_load
    def create_product(self, data, **kwargs):
        return Product(**data)
