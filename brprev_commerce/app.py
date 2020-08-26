from dynaconf import FlaskDynaconf, settings
from flask import Flask

from brprev_commerce import auth, views
from brprev_commerce.database import db


def create_app():
    app = Flask(__name__)

    FlaskDynaconf(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        settings.get('sqlalchemy_database_uri')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
        settings.get('sqlalchemy_track_modifications', False)

    db.init_app(app)
    views.init_app(app)
    auth.init_app(app)

    return app
