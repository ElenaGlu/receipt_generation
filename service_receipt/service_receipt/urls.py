from django.contrib import admin
from django.urls import path
from app_receipt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_order_for_receipt/', views.create_order_for_receipt, name='create_order_for_receipt')
]
