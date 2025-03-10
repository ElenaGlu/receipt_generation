import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create(client, order):
    # url = reverse('api-create')
    endpoint = '/api/create/'
    order_info = json.dumps(
        {
            'title': '1239',
            'restaurant': 'group-A',
        }
    )
    response = client.post(endpoint, order_info, content_type='application/json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_give_receipt_to_printer(client, order):
    url = reverse('give_receipt_to_printer')
    order_info = json.dumps(
        {
            'printer_id': 1
        }
    )
    response = client.post(url, order_info, content_type='application/json')
    assert response.status_code == 200
