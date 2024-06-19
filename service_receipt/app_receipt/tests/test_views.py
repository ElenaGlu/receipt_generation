import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_order_for_receipt(client, order):
    url = reverse('create_order_for_receipt')
    order_info = json.dumps(
        {
            'title': 'ABC',
            'restaurant': 'restaurant-A',
        }
    )
    response = client.post(url, order_info, content_type='application/json')
    # print(Order.objects.all().values())
    # print(Printer.objects.all().values())
    assert response.status_code == 201
