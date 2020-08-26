from http import HTTPStatus

import pytest
from freezegun import freeze_time

from brprev_commerce.database import db
from brprev_commerce.tests.factories import (CustomerFactory, ProductFactory,
                                             PurchaseFactory)


def test_init_purchase(app, auth_mock, auth_header):
    customer = CustomerFactory()
    db.session.flush()

    payload = {
        "data": {
             "type": "purchase",
             "attributes": {
                 "customer_id": customer.id
             }
        }
    }
    response = app.post('/api/v1/purchase', headers=auth_header,
                        json=payload)
    assert response.status_code == HTTPStatus.OK
    response_json = response.get_json()
    assert response.get_json() == {
        'data': {
            'attributes': {
                'closed_at': None,
                'created': response_json['data']['attributes']['created'],
                'customer_id': 1,
                'items': [],
                'state': 'PurchaseStates.OPENED',
                'subtotal': '0.00'
            },
            'id': '1',
            'type': 'purchase'
        }
    }


@pytest.mark.parametrize('payload,status_code,expected_response', [
    ({
        'data': {
            'attributes': {
                'customer_id': None
            },
            'type': 'purchase'
        }
    }, HTTPStatus.BAD_REQUEST, {
         'errors': [{
            'detail': 'Field may not be null.',
            'source': {'pointer': '/data/attributes/customer_id'}
         }]
    }), ({
        'data': {
            'attributes': {
                'customer_id': 99
            },
            'type': 'purchase'
        }
    }, HTTPStatus.BAD_REQUEST, {
        'errors': [{
            'detail': 'Customer ID=99 not found',
            'source': {'pointer': '/data/attributes/customer_id'}
        }]
    })
])
def test_init_purchase_with_invalid_payload(app, auth_mock, auth_header,
                                            payload, status_code,
                                            expected_response):
    response = app.post('/api/v1/purchase', headers=auth_header, json=payload)
    assert response.get_json() == expected_response
    assert response.status_code == status_code


def test_close_purchase(app, auth_mock, auth_header):
    purchase = PurchaseFactory()
    db.session.flush()
    response = app.delete(f'/api/v1/purchase/{purchase.id}',
                          headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    response_json = response.get_json()
    assert response_json == {
        'data': {
            'attributes': {
                'closed_at': response_json['data']['attributes']['closed_at'],
                'created': response_json['data']['attributes']['created'],
                'customer_id': 1,
                'items': [],
                'state': 'PurchaseStates.CLOSED',
                'subtotal': '0.00'
            },
            'id': '1',
            'type': 'purchase'
        }
    }


def test_close_purchase_already_closed(app, auth_mock, auth_header):
    purchase = PurchaseFactory()
    purchase.close()
    db.session.flush()
    previous_closed_at = purchase.closed_at
    response = app.delete(f'/api/v1/purchase/{purchase.id}',
                          headers=auth_header)
    assert response.status_code == 200

    closed_at = response.get_json()['data']['attributes']['closed_at']
    assert closed_at == previous_closed_at.strftime('%Y-%m-%dT%H:%M:%S.%f')


@pytest.mark.parametrize("payload,status_code,expected_response", [
    ({
        'data': {
            'attributes': {
                'description': 'Test Product 1',
                'price': '1.99'
            },
            'type': 'product'
        }
    }, HTTPStatus.OK, {
        'data': {
            'attributes': {
                'description': 'Test Product 1',
                'price': '2.00'
            },
            'id': '1',
            'type': 'product'
        }
    }), ({
        'data': {
            'attributes': {
                'price': '1.99'
            },
            'type': 'product'
        }
    }, HTTPStatus.BAD_REQUEST, {
        'errors': [{
            'detail': 'Missing data for required field.',
            'source': {'pointer': '/data/attributes/description'}
        }]
    }
    ), ({
        'data': {
            'attributes': {
                'price': 'price_string',
                'description': 'Test Product',
            },
            'type': 'product'
        }
    }, HTTPStatus.BAD_REQUEST, {
         'errors': [{
            'detail': 'Not a valid number.',
            'source': {
                'pointer': '/data/attributes/price'
            }
         }]
    }), ({
        'data': {
            'attributes': {
                'price': '10.99',
                'description': '',
            },
            'type': 'product'
        }
    }, HTTPStatus.BAD_REQUEST, {
        'errors': [{
            'detail': 'Invalid input.',
            'source': {
                'pointer': '/data/attributes/description'
            }
        }]
    })
])
def test_create_product(app, auth_mock, auth_header,
                        payload, status_code, expected_response):
    response = app.post('/api/v1/product', headers=auth_header, json=payload)
    assert response.status_code == status_code
    assert response.get_json() == expected_response


def test_add_item_to_purchase(app, auth_mock, auth_header):
    product = ProductFactory()
    purchase = PurchaseFactory()
    db.session.flush()

    payload = {
        'data': {
            'attributes': {
                'items': [{
                    'quantity': '2',
                    'product_id': product.id
                }]
            },
            'type': 'purchase',
            'id': str(purchase.id)
        }
    }
    response = app.patch('/api/v1/purchase', headers=auth_header, json=payload)
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.get_json() == {
        'data': {
            'attributes': {
                'closed_at': None,
                'created': response_json['data']['attributes']['created'],
                'customer_id': 1,
                'items': [{
                    'product_id': 1,
                    'quantity': 2,
                    'subtotal': '4.00'
                }],
                'state': 'PurchaseStates.OPENED',
                'subtotal': '4.00'
            },
            'id': '1',
            'type': 'purchase'
        }
    }


def test_add_item_to_a_nonexistent_purchase(app, auth_mock, auth_header):
    product = ProductFactory()
    db.session.flush()
    payload = {
        'data': {
            'attributes': {
                'items': [{
                    'quantity': '2',
                    'product_id': product.id
                }]
            },
            'type': 'purchase',
            'id': "99"
        }
    }
    response = app.patch('/api/v1/purchase', headers=auth_header, json=payload)
    assert response.status_code == 400
    assert response.get_json() == {
        'errors': [{
            'detail': 'Purchase ID=99 not found',
            'source': {'pointer': '/data/id'}
        }]
    }


def test_add_unexistent_product_to_a_purchase(app, auth_mock, auth_header):
    with freeze_time('2020-08-25'):
        purchase = PurchaseFactory()
    db.session.flush()

    payload = {
        'data': {
            'attributes': {
                'items': [{
                    'quantity': '2',
                    'product_id': 99
                }]
            },
            'type': 'purchase',
            'id': str(purchase.id)
        }
    }
    response = app.patch('/api/v1/purchase', headers=auth_header, json=payload)
    assert response.status_code == 400
    assert response.get_json() == {
        'errors': [{
            'detail': 'Product ID=99 not found',
            'source': {'pointer': '/data/attributes/items/0/product_id'}
        }]
    }
