from django.db import models


class CustomUser(models.Model):
    login = models.CharField(max_length=50, verbose_name='Имя пользователя в системе (никнейм)')
    password = models.CharField(max_length=30, verbose_name='Пароль пользователя')
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество пользователя')

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователи'


class Symptom(models.Model):
    name = models.CharField(verbose_name='Наименовение симптома', max_length=255)

    class Meta:
        verbose_name_plural = 'Симптомы'
        verbose_name = 'Симптом'


class Disease(models.Model):
    name = models.CharField(verbose_name='Наименовение болезни', max_length=255)
    symptoms = models.ManyToManyField(Symptom, verbose_name='Симптомы', related_name='diseases')

    class Meta:
        verbose_name_plural = 'Болезни'
        verbose_name = 'Болезнь'


class UserCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='card')
    disease = models.ManyToManyField(Disease, verbose_name='Болезни')

    class Meta:
        verbose_name_plural = 'Медицинские карты пользователей'
        verbose_name = 'Медицинская карта пользователя'


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
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=None)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    payment_method = models.CharField(choices=METHOD_PAYMENT, max_length=50)


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.TextField()


class CreditCard(models.Model):
    CVV = models.IntegerField()
    number = models.IntegerField()
    card_holder = models.CharField(max_length=100)
    exp_date = models.DateField()
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, default=None)
