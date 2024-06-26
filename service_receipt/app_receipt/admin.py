from django.contrib import admin

from app_receipt.models import Restaurant, Printer, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'printer')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass


