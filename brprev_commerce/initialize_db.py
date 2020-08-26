from brprev_commerce.app import create_app
from brprev_commerce.database import db


def initialize_db():
    app = create_app()
    with app.app_context():
        db.create_all(app=app)


if __name__ == '__main__':
    initialize_db()
