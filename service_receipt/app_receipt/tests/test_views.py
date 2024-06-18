import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_receipt_request(client, order):
    url = reverse('create_receipt_request')
    data = json.dumps(
        {
            'title': '1',
            'restaurant': 'restaurant-A',
        }
    )
    response = client.post(url, data, content_type='application/json')
    assert response.status_code == 201
