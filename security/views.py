from django.core.exceptions import ValidationError
from django.views.generic import View

from DVK_project.settings import CUSTOM_CSRF_TOKEN
from .sec import UserCheckMixin
from security.models import Session

from .models import CustomUser


class ProtectedView(View, UserCheckMixin):
    user_is_logged_in = False
    csrf_proceeded = False
    user: CustomUser = None

    def check_csrf_token(self):
        self.csrf_proceeded = self.request.COOKIES.get('custom_csrf_token', "") == CUSTOM_CSRF_TOKEN
        if not self.csrf_proceeded:
            raise ValidationError('csrf not proceeded')

    def get_user(self):
        sid = self.request.COOKIES.get('sid')
        login = self.request.POST.get('login')
        if sid is not None and sid != "undefined":
            self.user = Session.get_user_of_session(sid, self.request)
        if self.user is None and login is not None:
            self.user = CustomUser.objects.filter(login=login).first()

    def get(self, request):
        self.user_is_logged_in = self.user_has_session(request)
        self.get_user()

    def post(self, request):
        self.check_csrf_token()
        self.user_is_logged_in = self.user_has_session(request)
        self.get_user()
