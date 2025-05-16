import os
import datetime
from typing import Dict, List
from app_receipt.models import Order, Restaurant, Printer, Statuses
from django.db.models import F

from app_receipt.tasks import generate_PDF_task
from exceptions import AppError, ErrorType
import zipfile


class OrderReceipt:

    @staticmethod
    def create_order(request: Dict[str, str]) -> None:
        """
        Create an order for a receipt.
        :param request: dict containing keys - title, restaurant
        :raises AppError: This restaurant does not have a printer
        :raises AppError: Order with this header has already been created
        """
        title = request['title']
        restaurant = request['restaurant']
        if not Order.objects.filter(title=title):
            restaurant = Restaurant.objects.filter(title=restaurant).first()
            if restaurant:
                printers = list(Printer.objects.filter(restaurant_id=restaurant.id).values('id', 'print_queue'))
                if printers:
                    choose_printer = (min(printers, key=lambda x: x['print_queue']))['id']
                    Order.objects.create(title=title, printer_id=choose_printer)
                    Printer.objects.filter(id=choose_printer).update(print_queue=F("print_queue") + 1)
                    generate_PDF_task.delay(request)
                else:
                    raise AppError(
                        {
                            'error_type': ErrorType.ORDER_ERROR,
                            'description': 'this restaurant does not have a printer'
                        }
                    )
            else:
                raise AppError(
                    {
                        'error_type': ErrorType.ORDER_ERROR,
                        'description': 'the restaurant does not exist'
                    }
                )
        else:
            raise AppError(
                {
                    'error_type': ErrorType.ORDER_ERROR,
                    'description': 'it is forbidden to duplicate the receipt'
                }
            )

    @staticmethod
    def give_list_receipt(printer_id: int) -> str:
        """
        Return a list of receipts ready to be printed on a specific printer.
        :param printer_id: printer_id
        :raises AppError: there are no receipts for printing or the printer does not exist
        """
        orders = Order.objects.filter(printer_id=printer_id, status=Statuses.ready)
        title_orders = orders.values_list('title', flat=True)
        if title_orders:
            quantity_receipts = len(title_orders)
            zip_name = OrderReceipt.download_files(title_orders, printer_id)
            orders.update(status=Statuses.release)
            Printer.objects.filter(id=printer_id).update(print_queue=F("print_queue") - quantity_receipts)
            return zip_name
        else:
            raise AppError(
                {
                    'error_type': ErrorType.RECEIPT_ERROR,
                    'description': 'there are no receipts for printing or the printer does not exist'
                }
            )

    @staticmethod
    def download_files(files_to_zip: List[str], printer_id: int) -> str:
        """
        Compress and archive PDF to ZIP file.
        :param printer_id: printer_id
        :param files_to_zip: list containing the title of the orders
        :raises AppError: if there is an error creating the archive
        """
        try:
            current_time = datetime.datetime.now()
            zip_name = f'printer_{printer_id}_{current_time}.zip'
            zf = zipfile.ZipFile(f'app_receipt/media/PDF/{zip_name}', 'w')
            for file in files_to_zip:
                file = f'{file}.pdf'
                file_path = os.path.join('app_receipt/media/PDF/', file)
                zf.write(file_path)
            zf.close()
            # zip_file_receipts = open(f'app_receipt/media/PDF/{zip_name}', 'rb').read()
            return zip_name
        except Exception:
            raise AppError(
                {
                    'error_type': ErrorType.ARCHIVE_ERROR,
                    'description': 'archive creation error'
                }
            )
