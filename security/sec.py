import hashlib
import random
import datetime

from django.utils import timezone

from .models import Session
from index.models import CustomUser


class RSA:
    secret_key = None

    @staticmethod
    def prime_generator(max_lenght=1000):
        """ Return random prime number from 2 to max_lenght.
        Method: Решето Эратосфена

        """
        i = 2
        lst = []
        a = [i for i in range(max_lenght + 1)]
        a[1] = 0
        while i <= max_lenght:
            if a[i] != 0:
                lst.append(a[i])
                for j in range(i, max_lenght + 1, i):
                    a[j] = 0
            i += 1
        return lst[random.randint(0, len(lst))]

    @staticmethod
    def gcd(a, b):
        """Return the Greatest Common Divisor
        Возвращает НОД

        """
        while a != 0 and b != 0:
            if a > b:
                a %= b
            else:
                b %= a
        return a + b

    @classmethod
    def e_generator(cls, n, fi):
        e = n - 1
        while 0 < e < n:
            if cls.gcd(e, fi) == 1:
                return e
            e -= 1
        return -1

    @staticmethod
    def d_generator(e, fi):
        d = 0
        while (d * e) % fi != 1:
            d += 1
        return d

    @classmethod
    def rsa_keys(cls):
        p, q = [cls.prime_generator() for _ in range(2)]
        n = p * q
        fi = (p - 1) * (q - 1)
        open_key = cls.e_generator(n, fi)
        secret_key = cls.d_generator(open_key, fi)
        return (open_key, n), (secret_key, n)

    @staticmethod
    def encrypt(message, open_key):
        encrypt_message = ((ord(t) ** open_key[0]) % open_key[1] for t in message)
        return 'O'.join(str(i) for i in encrypt_message)

    @staticmethod
    def decrypt(encrypt_message, secret_key):
        message = ((int(c) ** secret_key[0]) % secret_key[1] for c in encrypt_message.split('O'))
        return ''.join(chr(i) for i in message)

    @classmethod
    def rsa_generator(cls):
        open_key, secret_key = cls.rsa_keys()
        return open_key, secret_key


OPEN_KEY_TUPLE, SECRET_KEY_TUPLE = RSA.rsa_generator()


class UserCheckMixin:
    user_session: Session = None
    current_user: CustomUser = None

    def user_has_session(self, request):
        self.delete_expired_sessions()
        self.user_session = self.get_user_session(request)
        if self.user_session is not None:
            self.current_user = self.user_session.user
            return True
        return False

    @staticmethod
    def delete_expired_sessions():
        for session in Session.objects.filter(expire_date__lt=datetime.datetime.now(tz=timezone.utc)):
            session.delete()

    @staticmethod
    def get_user_session(request):
        sid_str = request.COOKIES.get('sid', '')
        ip = request.META.get('REMOTE_ADDR')
        try:
            session_object = Session.objects.get(
                session_data=hashlib.sha3_256((sid_str + ip).encode('UTF-8')).hexdigest())
        except Session.DoesNotExist:
            return None
        return session_object
