import os
from typing import Dict
from app_receipt.models import Order, Restaurant, Printer
from django.db.models import F

from app_receipt.tasks import generate_PDF_task
from exceptions import AppError, ErrorType
import zipfile


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
    def give_list_receipt(request: Dict[str, int]):
        """
        Return a list of receipts ready to be printed on a specific printer.
        :param request: dict containing keys - printer_id
        :raises AppError: there are no receipts for printing or the printer does not exist
        """
        printer_id = request['printer_id']
        receipts = list(Order.objects.filter(printer_id=printer_id, status='READY').values('title'))
        if receipts:
            files = [d['title'] for d in receipts]
        else:
            raise AppError(
                {
                    'error_type': ErrorType.RECEIPT_ERROR,
                    'description': 'there are no receipts for printing or the printer does not exist'
                }
            )
        buffer = OrderReceipt.download_files(files)
        for title in files:
            Order.objects.filter(title=title).update(status='RELEASE')
        return buffer


    @staticmethod
    def download_files(files_to_zip):
        zip_name = 'receipt.zip'
        zf = zipfile.ZipFile(zip_name, 'w')
        for file in files_to_zip:
            file = f'{file}.pdf'
            file_path = os.path.join('/home/elena/lena/receipt_generation/service_receipt/app_receipt/media/PDF/', file)
            zf.write(file_path)
        zf.close()
        file = open(zip_name, 'rb').read()
        return file



