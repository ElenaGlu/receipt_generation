import json

from django.http import FileResponse
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .app_services import OrderReceipt
from .schemas import CREATE_RECEIPT, GET_RECEIPT


@method_decorator(*CREATE_RECEIPT)
@method_decorator(*GET_RECEIPT)
class Receipt(viewsets.GenericViewSet):
    @action(methods=['POST'], detail=False, url_path='create')
    def create_receipt(self, request: Request) -> Response:
        """
        Create an order for a receipt.
        :param request: JSON object containing keys - title, restaurant
        :return: "created" (201) response code
        :raises AppError: This restaurant does not have a printer
        :raises AppError: Order with this header has already been created
        """
        obj = OrderReceipt()
        obj.create_order(json.loads(request.body))
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False, url_path='get')
    def get_receipt(self, request: Request) -> FileResponse:
        """
            Return a list of receipts ready to be printed on a specific printer.
            :param request: JSON object containing keys - printer_id
            :return: zip-file
            :raises AppError: there are no receipts for printing or the printer does not exist
            """
        obj = OrderReceipt()
        zip_name = obj.give_list_receipt(request.GET.get('printer_id'))
        zip_file_receipts = open(f'app_receipt/media/PDF/{zip_name}', 'rb').read()
        response = FileResponse(zip_file_receipts, as_attachment=True, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + zip_name
        return response
