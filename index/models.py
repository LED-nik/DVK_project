from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()


class Order(models.Model):
    CASH = 'Cash'
    CARD = 'Card'
    METHOD_PAYMENT = [
        (CASH, 'Cash'),
        (CARD, 'Card')
    ]
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    count = models.IntegerField()
#   user_id = models.ForeignKey('User', on_delete=models.CASCADE())
    address_id = models.ForeignKey('Address', on_delete=models.CASCADE)
    payment_method = models.CharField(choices=METHOD_PAYMENT, max_length=50)


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.TextField()


class CreditCard(models.Model):
    CVV = models.IntegerField()
    number = models.IntegerField()
    card_holder = models.CharField(max_length=100)
    exp_date = models.DateField()
#   user_id = models.ForeignKey('User', on_delete=models.CASCADE())S


