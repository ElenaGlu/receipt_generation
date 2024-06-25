from django.contrib import admin
from django.urls import path
from app_receipt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_order_for_receipt/', views.create_order_for_receipt, name='create_order_for_receipt'),
    path('give_receipt_to_printer/', views.give_receipt_to_printer, name='give_receipt_to_printer')
]
