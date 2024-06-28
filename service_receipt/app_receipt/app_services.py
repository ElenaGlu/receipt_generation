import os
import datetime
from typing import Dict, List, Tuple
from app_receipt.models import Order, Restaurant, Printer
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
    def give_list_receipt(printer_id: int) -> Tuple[bytes, str]:
        """
        Return a list of receipts ready to be printed on a specific printer.
        :param printer_id: printer_id
        :raises AppError: there are no receipts for printing or the printer does not exist
        """
        receipts = Order.objects.filter(printer_id=printer_id, status='READY')
        receipts_values = list(receipts.values('title'))
        if receipts:
            title_receipts = [d['title'] for d in receipts_values]
            quantity_receipts = len(title_receipts)
        else:
            raise AppError(
                {
                    'error_type': ErrorType.RECEIPT_ERROR,
                    'description': 'there are no receipts for printing or the printer does not exist'
                }
            )
        zip_file_receipts, zip_name = OrderReceipt.download_files(title_receipts, printer_id)
        receipts.update(status='RELEASE')
        Printer.objects.filter(id=printer_id).update(print_queue=F("print_queue") - quantity_receipts)
        return zip_file_receipts, zip_name

    @staticmethod
    def download_files(files_to_zip: List[str], printer_id: int) -> Tuple[bytes, str]:
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
            zip_file_receipts = open(f'app_receipt/media/PDF/{zip_name}', 'rb').read()
            return zip_file_receipts, zip_name
        except Exception:
            raise AppError(
                {
                    'error_type': ErrorType.ARCHIVE_ERROR,
                    'description': 'archive creation error'
                }
            )
