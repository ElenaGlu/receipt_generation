import pytest


@pytest.mark.django_db
def test_create_receipt_success(api_client, order):
    payload = {
        'title': '1234',
        'restaurant': 'group-A'
    }
    response = api_client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_receipt_duplicate_title(api_client, order):
    payload = {
        'title': '1239',
        'restaurant': 'group-A'
    }
    response = api_client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_receipt_no_printer_for_restaurant(api_client, restaurant):
    payload = {
        'title': '9999',
        'restaurant': 'group-E'
    }
    response = api_client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.parametrize('payload', [
    {'restaurant': 'group-A'},  # без title
    {'title': '1234'},  # без restaurant
    {},  # пустой
])
def test_create_receipt_invalid_payload(api_client, payload):
    response = api_client.post('/api/create/', data=payload, format='json')
    assert response.status_code == 400
