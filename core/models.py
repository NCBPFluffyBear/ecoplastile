from django.conf import settings
from django.db import models

# Create your models here.

# Logic of storing order, adding item to order
# Store bool if ordered


class Item(models.Model):
    title = models.CharField(max_length=100)

    # computes the "informal" string representations of an object
    def __str__(self):
        return self.title


# Links Order and Item
class OrderItem(models.Model):
    item = models.ForeignKey(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # to add order items to order
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    # set when item is ordered
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
