from django.http.response import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

from index.models import CustomUser
from security.models import Session
from security.views import ProtectedView


class LogInView(ProtectedView):
    def post(self, request):
        super().post(request)
        if not self.user_is_logged_in:
            login = request.POST.get('login', '')
            password = request.POST.get('password', '')
            try:
                user = CustomUser.objects.get(login=login, password=password)
            except CustomUser.DoesNotExist:
                return JsonResponse({'message': 'Нет такого пользователя в системе! Проверьте логин и пароль.'},
                                    status=404)
            sid_str = Session.create_session(request, user)
        return JsonResponse({'csrf': get_token(request), 'sid': sid_str or '', 'redirect_url': '/welcome'})

    def get(self, request):
        return render(request, 'index/reg-auth.html',
                      {'csrf': get_token(request)})  # TODO: поменять на custom_csrf_token и проверять его


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
        user_object.password = request.POST.get('password')
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
