from datetime import timedelta

from flask_jwt import JWT
from sqlalchemy.orm.exc import NoResultFound

from brprev_commerce.models import User


def init_app(app):
    app.config['SECRET_KEY'] = 'U44fJ%$LIJl&%hUald5pP'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=600)
    app.config['JWT_AUTH_URL_RULE'] = '/api/v1/auth'
    JWT(app, authenticate, identity)


def authenticate(login, password):
    try:
        user = User.get_one_by(login=login, password=password)
    except NoResultFound:
        return
    return user


def identity(payload):
    try:
        user = User.get_one(id=payload['identity'])
    except NoResultFound:
        return
    return user
