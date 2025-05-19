import pytest
from rest_framework.test import APIClient
from logging import getLogger

logger = getLogger()
client = APIClient()


@pytest.mark.django_db
def test_create_receipt_success(order):
    payload = {
        'title': '1239',
        'restaurant': 'group-A'
    }
    response = client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_receipt_success(order):
    payload = {
        'printer_id': 1
    }
    response = client.get('/api/get/', data=payload, format='json')

    logger.info(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_receipt_duplicate_title(order):
    payload = {
        'title': '0022',
        'restaurant': 'group-A'
    }
    response = client.post('/api/create/', data=payload, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_receipt_no_printer_for_restaurant(restaurant):
    payload = {
        'title': '9999',
        'restaurant': 'group-E'
    }
    response = client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_receipt_invalid_payload():
    payload = {
        'restaurant': 'group-A'
    }
    response = client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 400
