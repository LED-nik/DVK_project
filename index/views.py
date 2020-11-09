import datetime
import hashlib

from django.http.response import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

from index.models import CustomUser
from security.sec import OPEN_KEY_TUPLE, SECRET_KEY_TUPLE, RSA
from security.models import Session, EncryptionKeys
from security.views import ProtectedView


class LogInView(ProtectedView):
    def post(self, request):
        super().post(request)
        if not self.user_is_logged_in:
            login = request.POST.get('login', '')
            password = request.POST.get('password', '')
            decrypted_password = RSA.decrypt(password, SECRET_KEY_TUPLE)
            hash_password = hashlib.sha3_256(decrypted_password.encode('UTF-8')).hexdigest()
            try:
                user = CustomUser.objects.get(login=login, password=hash_password)
            except CustomUser.DoesNotExist:
                return JsonResponse({'message': 'Нет такого пользователя в системе! Проверьте логин и пароль.'},
                                    status=404)
            sid_str = Session.create_session(request, user)
        return JsonResponse({'csrf': get_token(request), 'sid': sid_str or '', 'redirect_url': '/welcome'})

    def get(self, request):
        open_key = OPEN_KEY_TUPLE[0]
        secret_key = SECRET_KEY_TUPLE[0]
        n = OPEN_KEY_TUPLE[1]
        EncryptionKeys.objects.create(open_key=open_key, secret_key=secret_key, n_element=n,
                                      expire_date=datetime.datetime.now() + datetime.timedelta(minutes=5))
        response = render(request, 'index/reg-auth.html',
                      {'csrf': get_token(request), 'open_key': open_key,
                       'n': n})  # TODO: поменять на custom_csrf_token и проверять его, а не встроенный
        response.set_cookie(key='open_key', value=open_key)
        response.set_cookie(key='n', value=n)
        return response


class LogOutView(ProtectedView):
    def get(self, request):
        super().get(request)
        if self.user_is_logged_in:
            self.user_session.delete()
        return render(request, 'index/reg-auth.html', {'csrf': get_token(request)})


class UserCreateView(ProtectedView):
    def post(self, request):
        user_object = CustomUser()
        user_object.name = request.POST.get('name')
        user_object.last_name = request.POST.get('last_name')
        user_object.patronymic = request.POST.get('patronymic')
        user_object.password = hashlib.sha3_256(request.POST.get('password').encode('UTF-8')).hexdigest()
        user_object.login = request.POST.get('login')
        user_object.save()
        return HttpResponse()


class MainPageView(ProtectedView):
    def get(self, request):
        super().get(request)
        if self.user_is_logged_in:
            return render(request, 'index/main.html', {'csrf': get_token(request)})
        else:
            return render(request, 'index/reg-auth.html', {'csrf': get_token(request)})
