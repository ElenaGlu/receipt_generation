import pytest

from app_receipt import models
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture()
def restaurant():
    restaurant = [
        "group-A",
        "group-B",
        "group-C",
        "group-D",
        "group-E"
    ]
    temporary = []
    for idx, obj in enumerate(restaurant):
        temporary.append(models.Restaurant(id=idx + 1, title=obj))
    return models.Restaurant.objects.bulk_create(temporary)


@pytest.fixture()
def printer(restaurant):
    printer = [
        {
            "id": 1,
            "title": "printer_A1",
            "restaurant_id": restaurant[0].id,
            "print_queue": 1
        },
        {
            "id": 2,
            "title": "printer_A2",
            "restaurant_id": restaurant[0].id,
            "print_queue": 2
        },
        {
            "id": 3,
            "title": "printer_B1",
            "restaurant_id": restaurant[1].id,
            "print_queue": 0
        },
        {
            "id": 4,
            "title": "printer_C1",
            "restaurant_id": restaurant[2].id,
            "print_queue": 0
        },
        {
            "id": 5,
            "title": "printer_D1",
            "restaurant_id": restaurant[3].id,
            "print_queue": 0
        },

    ]
    temp = [models.Printer(**obj) for obj in printer]
    return models.Printer.objects.bulk_create(temp)


@pytest.fixture()
def order(printer):
    order = [
        {
            "id": 2,
            "title": "0011",
            "status": "CREATE",
            "printer_id": printer[0].id
        },
        {
            "id": 3,
            "title": "1239",
            "status": "READY",
            "printer_id": printer[0].id
        }

    ]
    temp = [models.Order(**obj) for obj in order]
    return models.Order.objects.bulk_create(temp)
