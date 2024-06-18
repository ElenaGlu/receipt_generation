from django.contrib import admin
from django.urls import path
from app_receipt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_receipt_request/', views.create_receipt_request, name='create_receipt_request')
]
