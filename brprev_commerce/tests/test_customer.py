import pytest


def test_create_customer(app, auth_header, auth_mock):
    payload = {
        "data": {
            "type": "customer",
            "attributes": {
                "name": "Teste da Silva"
            }
        }
    }
    response = app.post('/api/v1/customer', headers=auth_header, json=payload)
    assert response.status_code == 200
    assert response.get_json() == {
        'data': {
            'attributes': {
                'name': 'Teste da Silva'
            },
            'id': '1',
            'type': 'customer'
        }
    }


@pytest.mark.parametrize("payload,expected_response", [
    ({}, {
        'errors': [
            {
                'detail': 'Object must include `data` key.',
                'source': {
                    'pointer': '/'
                }
            }
        ]
    }),
    ({"name": ""}, {
        'errors': [
            {
                'detail': 'Object must include `data` key.',
                'source': {
                    'pointer': '/'
                }
            }
        ]
    }),
    ({
        "data": {
            "type": "customer",
            "attributes": {
                "name": ""
            }
        }
    }, {
        'errors': [
            {
                'detail': 'Invalid input.',
                'source': {
                    'pointer': '/data/attributes/name'
                }
            }
        ]
    })
])
def test_create_customer_with_invalid_payload(app, auth_mock, auth_header,
                                              payload, expected_response):
    response = app.post('/api/v1/customer', headers=auth_header, json=payload)
    assert response.status_code == 400
    assert response.get_json() == expected_response
