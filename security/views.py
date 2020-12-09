from django.core.exceptions import ValidationError
from django.views.generic import View

from DVK_project.settings import CUSTOM_CSRF_TOKEN
from .sec import UserCheckMixin


class ProtectedView(View, UserCheckMixin):
    user_is_logged_in = False
    csrf_proceeded = False

    def check_csrf_token(self):
        self.csrf_proceeded = self.request.COOKIES.get('custom_csrf_token', "") == CUSTOM_CSRF_TOKEN
        if not self.csrf_proceeded:
            raise ValidationError('csrf not proceeded')

    def get(self, request):
        self.user_is_logged_in = self.user_has_session(request)

    def post(self, request):
        self.check_csrf_token()
        self.user_is_logged_in = self.user_has_session(request)
