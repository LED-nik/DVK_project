from django.urls import path, include

from .views import MainView

urlpatterns = [
    path('', MainView.as_view())
]