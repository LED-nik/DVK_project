import datetime
import hashlib
from django.db import models

from index.models import CustomUser


class Session(models.Model):
    session_data = models.TextField(verbose_name='Хаш пользователя')
    expire_date = models.DateTimeField(verbose_name='Срок истечения сессии')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='session',
                             verbose_name='Активная сессия пользователя')

    @classmethod
    def generate_sid(cls):
        last_id = cls.objects.values_list('id', flat=True).order_by('id').last()
        unique_sid = hashlib.sha3_256(str(last_id).encode('UTF-8')).hexdigest()
        return unique_sid

    @classmethod
    def create_session(cls, request, user):
        sid_str = cls.generate_sid()
        ip = request.META.get('REMOTE_ADDR')
        session_data = hashlib.sha3_256((sid_str + ip).encode('UTF-8')).hexdigest()
        Session.objects.create(session_data=session_data,
                               expire_date=datetime.datetime.now() + datetime.timedelta(minutes=5), user=user)
        return sid_str

    @classmethod
    def get_user_of_session(cls, sid, request):
        ip = request.META.get('REMOTE_ADDR')
        return cls.objects.get(session_data=hashlib.sha3_256((sid + ip).encode('UTF-8')).hexdigest()).user


class EncryptionKeys(models.Model):
    open_key = models.BigIntegerField(verbose_name='Открытый ключ')
    secret_key = models.BigIntegerField(verbose_name='Закрытый ключ')
    n_element = models.BigIntegerField(verbose_name='Важный элемент n, без которого шифрование не работает')
    expire_date = models.DateTimeField(verbose_name='Срок истечения времени жизни ключей')