import json

from django.http import HttpRequest, HttpResponse

from app_receipt.app_services import OrderReceipt


def create_order_for_receipt(request: HttpRequest) -> HttpResponse:

    """
    Create an order for a receipt
    :param request: JSON object containing keys - title, restaurant
    :return: "created" (201) response code
    :raises
    """
    if request.method == "POST":
        obj = OrderReceipt()
        obj.add_order(json.loads(request.body))
        return HttpResponse(status=201)

