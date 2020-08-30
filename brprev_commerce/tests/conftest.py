import pytest
from werkzeug.datastructures import Headers

from brprev_commerce.app import create_app
from brprev_commerce.database import db


@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.drop_all(app=app)
        db.create_all(app=app)
        yield app.test_client()


@pytest.fixture(scope="function")
def auth_header(app, truncate):
    create_payload = {
        "data": {
            "type": "user",
            "attributes": {
                "login": "test_user",
                "password": "1234567a"
            }
        }
    }
    response = app.post('/api/v1/user', json=create_payload)
    login_payload = {
        "username": "test_user",
        "password": "1234567a"
    }
    response = app.post('/api/v1/auth', json=login_payload)
    access_token = f'JWT {response.get_json()["access_token"]}'
    return Headers({'Authorization': access_token})


@pytest.fixture(scope="function")
def truncate(app):
    for table in db.metadata.sorted_tables:
        db.session.execute(f'TRUNCATE {table.name} RESTART IDENTITY CASCADE')
    db.session.commit()
