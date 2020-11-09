from django.urls import path

from .views import LogInView, UserCreateView, MainPageView, LogOutView, ChatView

urlpatterns = [
    path('', LogInView.as_view()),
    path('create_user', UserCreateView.as_view()),
    path('welcome', MainPageView.as_view()),
    path('log_out', LogOutView.as_view()),
    path('send_message', ChatView.as_view()),
]
