from django.db import models


class Restaurant(models.Model):
    title = models.CharField(max_length=100)


class Printer(models.Model):
    title = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Order(models.Model):
    title = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


STATUS = {
    "CREATE": "in the creation queue",
    "READY": "ready to print",
    "RELEASE": "release"
}


class Receipt(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=7, choices=STATUS)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
