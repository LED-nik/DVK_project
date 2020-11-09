from django.views.generic import View

from .sec import UserCheckMixin


class ProtectedView(View, UserCheckMixin):
    user_is_logged_in = False

    def get(self, request):
        self.user_is_logged_in = self.user_has_session(request)

    def post(self, request):
        self.user_is_logged_in = self.user_has_session(request)
