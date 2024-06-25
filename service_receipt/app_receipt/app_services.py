from typing import Dict
from django.http import HttpResponse
from app_receipt.models import Order, Restaurant, Printer
from django.db.models import F

from app_receipt.tasks import generate_PDF_task
from exceptions import AppError, ErrorType


class OrderReceipt:

    @staticmethod
    def add_order(request: Dict[str, str]) -> None:
        """
        Create an order for a receipt.
        :param request: dict containing keys - title, restaurant
        :raises AppError: This restaurant does not have a printer
        :raises AppError: Order with this header has already been created
        """
        title = request['title']
        restaurant = request['restaurant']
        if not Order.objects.filter(title=title):
            restaurant_id = Restaurant.objects.filter(title=restaurant).first().id
            printer = list(Printer.objects.filter(restaurant_id=restaurant_id).values('id', 'print_queue'))
            if printer:
                choose_printer = (min(printer, key=lambda x: x['print_queue']))['id']
                Order.objects.create(title=title, printer_id=choose_printer)
                Printer.objects.filter(id=choose_printer).update(print_queue=F("print_queue") + 1)
                generate_PDF_task.delay(request)
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.PRINTER_ERROR,
                        'description': 'This restaurant does not have a printer'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.ORDER_ERROR,
                    'description': 'Order with this header has already been created'
                }
            )

    @staticmethod
    def give_list_receipt(request: Dict[str, str]):
        """
        Return a list of receipts ready to be printed on a specific printer.
        :param request: dict containing keys - printer_id
        :raises AppError: there are no receipts for printing or the printer does not exist
        """
        printer_id = request['printer_id']
        receipts = list(Order.objects.filter(printer=printer_id, status='READY').values('title'))
        if receipts:
            for d in receipts:
                obj = d['title']
                file_name = f'{obj}.pdf'
                with open(f'/home/elena/lena/receipt_generation/service_receipt/app_receipt/media/PDF/{file_name}',
                          'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = filename = file_name
        else:
            raise AppError(
                {
                    'error_type': ErrorType.RECEIPT_ERROR,
                    'description': 'there are no receipts for printing or the printer does not exist'
                }
            )
