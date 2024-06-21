from typing import Dict

from app_receipt.models import Order, Restaurant, Printer
from django.db.models import F

from app_receipt.tasks import generate_PDF_task


class OrderReceipt:

    @staticmethod
    def add_order(request: Dict[str, str]):
        title = request['title']
        restaurant = request['restaurant']
        if not Order.objects.filter(title=title):
            restaurant_id = Restaurant.objects.filter(title=restaurant).first().id
            printer_id = list(Printer.objects.filter(restaurant_id=restaurant_id).values('id', 'print_queue'))
            if printer_id:
                d = min(printer_id, key=lambda x: x['print_queue'])
                choose_printer = d['id']
                Order.objects.create(title=title, printer_id=choose_printer)
                Printer.objects.filter(id=choose_printer).update(print_queue=F("print_queue") + 1)
                generate_PDF_task.delay(request)
            else:
                raise
        else:
            raise
