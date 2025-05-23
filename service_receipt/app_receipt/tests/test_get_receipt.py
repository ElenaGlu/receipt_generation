import pytest
from app_receipt.models import Statuses


@pytest.mark.django_db
def test_get_receipt_success(api_client, order):
    payload = {
        'printer_id': 1
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_receipt_invalid_printer_id(api_client, order):
    payload = {
        'printer_id': 999
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_receipt_no_ready_orders(api_client, order):
    from app_receipt.models import Order
    Order.objects.all().update(status=Statuses.release)
    payload = {
        'printer_id': 1
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_receipt_file_content_type(api_client, order):
    payload = {
        'printer_id': 1
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response['Content-Type'] == 'application/zip'


@pytest.mark.django_db
def test_get_receipt_updates_order_status(api_client, order):
    from app_receipt.models import Order
    payload = {
        'printer_id': 1
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response.status_code == 200

    updated_orders = Order.objects.filter(printer_id=1, title='1239')
    for o in updated_orders:
        assert o.status == Statuses.release


@pytest.mark.django_db
def test_get_receipt_decrements_print_queue(api_client, order):
    from app_receipt.models import Printer
    payload = {
        'printer_id': 1
    }
    response = api_client.get('/api/get/', data=payload, format='zip')
    assert response.status_code == 200

    printer_obj = Printer.objects.get(id=1)
    assert printer_obj.print_queue == 0
