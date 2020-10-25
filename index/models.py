from django.db import models


# Create your models here.

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
