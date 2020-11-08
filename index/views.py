from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class MainView(View):
    template_name = 'index/reg-auth.html'

    def get(self, request):
        return render(request, 'index/reg-auth.html', {'csrf': get_token(request)})

