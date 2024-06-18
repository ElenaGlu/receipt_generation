from typing import Dict

from app_receipt.models import Order, Restaurant, Printer


class OrderReceipt:

    @staticmethod
    def add_order(request: Dict[str, str]):
        title = request['title']
        restaurant = request['restaurant']
        if not Order.objects.filter(title=title):
            restaurant_id = Restaurant.objects.get(title=restaurant).id
            printer_id = list(Printer.objects.filter(restaurant_id=restaurant_id).values('id'))
            if printer_id:
                # choice printer
                Order.objects.create(**request)
            else:
                raise
        else:
            raise
