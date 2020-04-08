from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def increase_inventory(self, amount):
        self.inventory += amount
        self.save()

    def decrease_inventory(self, amount):
        if self.inventory >= amount:
            self.inventory -= amount
            self.save()
        else:
            raise Exception('Inventory is not enough')


class OrderRow(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    amount = models.IntegerField()

    def __str__(self):
        return '{} - {} - {}'.format(self.product, self.order, self.amount)


class Order(models.Model):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.PROTECT)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()

    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    status_choices = (
        (STATUS_SHOPPING, 'shopping'),
        (STATUS_SUBMITTED, 'submitted'),
        (STATUS_CANCELED, 'canceled'),
        (STATUS_SENT, 'sent'),
    )
    status = models.IntegerField(choices=status_choices)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.customer, self.order_time, self.total_price, self.status)

    @staticmethod
    def initiate(customer):
        customer.balance += 20000

    def add_product(self, product, amount):
        pass
        #  += (product * amount)

    def remove_product(self, product, amount=None):
        pass
        #  -= (product * amount)

    def submit(self):
        assert self.status == Order.STATUS_SHOPPING, 'Status is not shopping'
        ###
        self.status = Order.STATUS_SUBMITTED
        self.save()

    def cancel(self):
        if (self.status == Order.STATUS_SUBMITTED) and (self.status != Order.STATUS_SENT):
            self.status = Order.STATUS_CANCELED
            ####
            self.save()
        else:
            raise Exception('Order has not been submitted or has been sent before')

    def send(self):
        if self.status == Order.STATUS_SUBMITTED:
            self.status = Order.STATUS_SENT
            self.save()
        else:
            raise Exception('Order has not been submitted')
