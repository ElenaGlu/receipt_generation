from django.db import models


class Restaurant(models.Model):
    title = models.CharField(max_length=100)


class Printer(models.Model):
    title = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    print_queue = models.IntegerField(default=0)


STATUS = {
    "CREATE": "in the creation queue",
    "READY": "ready to print",
    "RELEASE": "release"
}


class Order(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=7, choices=STATUS, default='CREATE')
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
