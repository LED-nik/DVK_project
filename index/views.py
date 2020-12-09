import datetime
import hashlib
import secrets

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from DVK_project.settings import SECURE, CUSTOM_CSRF_TOKEN
from index.models import CustomUser
from security.models import Session, EncryptionKeys
from security.sec import OPEN_KEY_TUPLE, SECRET_KEY_TUPLE, RSA
from security.views import ProtectedView


class LogInView(ProtectedView):
    def post(self, request):
        try:
            super().post(request)
        except ValidationError:
            return HttpResponse(status=403)
        if not self.user_is_logged_in:
            login = request.POST.get('login', '')
            password = request.POST.get('password', '')
            decrypted_password = RSA.decrypt(password, SECRET_KEY_TUPLE) if SECURE else password  # TODO:убрать
            salt = self.user.salt if self.user is not None else ""
            hash_password = hashlib.sha3_256((decrypted_password + salt).encode('UTF-8')).hexdigest()
            try:
                user = CustomUser.objects.get(login=login, password=hash_password)
            except CustomUser.DoesNotExist:
                return JsonResponse({'message': 'Нет такого пользователя в системе! Проверьте логин и пароль.'},
                                    status=404)
            sid_str = Session.create_session(request, user)
        return JsonResponse({'sid': sid_str or '', 'redirect_url': '/welcome'})

    def get(self, request):
        open_key = OPEN_KEY_TUPLE[0]
        secret_key = SECRET_KEY_TUPLE[0]
        n = OPEN_KEY_TUPLE[1]
        EncryptionKeys.objects.create(open_key=open_key, secret_key=secret_key, n_element=n,
                                      expire_date=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(
                                          minutes=5))
        response = render(request, 'index/reg-auth.html')
        response.set_cookie(key='open_key', value=open_key)
        response.set_cookie(key='n', value=n)
        response.set_cookie(key='custom_csrf_token', value=CUSTOM_CSRF_TOKEN)
        return response


class LogOutView(ProtectedView):
    def get(self, request):
        super().get(request)
        if self.user_is_logged_in:
            self.user_session.delete()
        response = render(request, 'index/reg-auth.html')
        response.set_cookie(key='custom_csrf_token', value=CUSTOM_CSRF_TOKEN)
        return response


class UserCreateView(ProtectedView):
    def post(self, request):
        try:
            super().post(request)
        except ValidationError:
            return HttpResponse(status=403)
        try:
            user_object = CustomUser()
            user_object.name = request.POST.get('name')
            user_object.last_name = request.POST.get('last_name')
            user_object.patronymic = request.POST.get('patronymic')
            salt = secrets.token_hex(16)
            user_object.salt = salt
            user_object.password = hashlib.sha3_256((request.POST.get('password') + salt).encode('UTF-8')).hexdigest()
            user_object.login = request.POST.get('login')

            user_object.save()
        except IntegrityError:
            return HttpResponse("Пользователь уже существует", status=500)
        return HttpResponse(status=200)


class ChatView(ProtectedView):
    def post(self, request):
        try:
            super().post(request)
        except ValidationError:
            return HttpResponse(status=403)
        if self.user_is_logged_in:
            message = request.POST.get('message', '')
            decrypted_message = RSA.decrypt(message, SECRET_KEY_TUPLE) if SECURE else message  # TODO: убрать
            return JsonResponse({'answer': 'Вы написали: {}'.format(decrypted_message)}, status=200)


class MainPageView(ProtectedView):
    def get(self, request):
        super().get(request)
        if self.user_is_logged_in:
            return render(request, 'index/main.html')
        else:
            return render(request, 'index/reg-auth.html')
