import json

from django.http import HttpRequest, HttpResponse

from app_receipt.app_services import OrderReceipt


def create_order_for_receipt(request: HttpRequest) -> HttpResponse:
    """
    Create an order for a receipt.
    :param request: JSON object containing keys - title, restaurant
    :return: "created" (201) response code
    :raises AppError: This restaurant does not have a printer
    :raises AppError: Order with this header has already been created
    """
    if request.method == "POST":
        obj = OrderReceipt()
        obj.add_order(json.loads(request.body))
        return HttpResponse(status=201)


def give_receipt_to_printer(request: HttpRequest) -> HttpResponse:
    """
    Return a list of receipts ready to be printed on a specific printer.
    :param request: JSON object containing keys - printer_id
    :return: "OK" (200) response code
    :raises
    """
    if request.method == "GET":
        obj = OrderReceipt()
        zip_file_receipts, zip_name = obj.give_list_receipt(request.GET.get('printer_id'))
        response = HttpResponse(zip_file_receipts, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + zip_name
        return response
