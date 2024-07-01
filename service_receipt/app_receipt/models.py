from django.db import models


class Restaurant(models.Model):
    title = models.CharField(max_length=100)


class Printer(models.Model):
    title = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    print_queue = models.PositiveIntegerField(default=0)


class Statuses(models.TextChoices):
    create = 'CREATE'
    ready = 'READY'
    release = 'RELEASE'


class Order(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=7, choices=Statuses.choices, default='CREATE')
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
