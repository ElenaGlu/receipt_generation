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



# @pytest.mark.django_db
# def test_give_receipt_to_printer(client, order):
#     url = reverse('give_receipt_to_printer')
#     order_info = json.dumps(
#         {
#             'printer_id': 1
#         }
#     )
#     response = client.post(url, order_info, content_type='application/json')
#     assert response.status_code == 200
