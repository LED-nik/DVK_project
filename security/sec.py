import random


class RSA:
    secret_key = None

    @staticmethod
    def prime_generator(count=2, max_lenght=1000):
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

    def e_generator(self, n, fi):
        e = n - 1
        while 0 < e < n:
            if self.gcd(e, fi) == 1:
                return e
            e -= 1
        return -1

    @staticmethod
    def d_generator(e, fi):
        d = 0
        while (d * e) % fi != 1:
            d += 1
        return d

    def rsa_keys(self):
        p, q = [self.prime_generator() for _ in range(2)]
        n = p * q
        fi = (p - 1) * (q - 1)
        e = self.e_generator(n, fi)
        d = self.d_generator(e, fi)
        return (e, n), (d, n)

    @staticmethod
    def encrypt(message, open_key):
        encrypt_message = ((ord(t) ** open_key[0]) % open_key[1] for t in message)
        return 'O'.join(str(i) for i in encrypt_message)

    @staticmethod
    def decrypt(encrypt_message, secret_key):
        message = ((int(c) ** secret_key[0]) % secret_key[1] for c in encrypt_message.split('O'))
        return ''.join(chr(i) for i in message)

    def rsa_generator(self):
        open_key, secret_key = self.rsa_keys()
        return open_key, secret_key

    def decrypting(self, encrypt_message):
        decrypt_message = self.decrypt(encrypt_message, self.secret_key)
