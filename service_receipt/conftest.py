import pytest

from app_receipt import models


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
        {
            "id": 4,
            "title": "printer_C1",
            "restaurant_id": restaurant[2].id
        },
        {
            "id": 5,
            "title": "printer_D1",
            "restaurant_id": restaurant[3].id
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
            "title": "0011",
            "status": "CREATE",
            "printer_id": printer[0].id
        },
        {
            "id": 3,
            "title": "0022",
            "status": "READY",
            "printer_id": printer[0].id
        }

    ]
    temporary = []
    for obj in order:
        temporary.append(models.Order(**obj))
    return models.Order.objects.bulk_create(temporary)