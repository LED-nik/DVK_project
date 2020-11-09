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
