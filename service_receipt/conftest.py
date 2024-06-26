import pytest

from app_receipt import models


@pytest.fixture()
def restaurant():
    restaurant = [
        "restaurant-A",
        "restaurant-B",
        "restaurant-C"
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
            "restaurant_id": restaurant[0].id
        },
        {
            "id": 2,
            "title": "printer_A2",
            "restaurant_id": restaurant[0].id
        },
        {
            "id": 3,
            "title": "printer_B1",
            "restaurant_id": restaurant[1].id
        },

    ]
    temporary = []
    for obj in printer:
        temporary.append(models.Printer(**obj))
    return models.Printer.objects.bulk_create(temporary)


@pytest.fixture()
def order(printer):
    order = [
        {
            "id": 2,
            "title": "order1",
            "status": "CREATE",
            "printer_id": printer[0].id
        },
        {
            "id": 3,
            "title": "order1",
            "status": "READY",
            "printer_id": printer[0].id
        }

    ]
    temporary = []
    for obj in order:
        temporary.append(models.Order(**obj))
    return models.Order.objects.bulk_create(temporary)
