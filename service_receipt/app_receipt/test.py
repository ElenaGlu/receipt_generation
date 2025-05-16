import pytest
from rest_framework.test import APIClient

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
    assert response.status_code == 200
