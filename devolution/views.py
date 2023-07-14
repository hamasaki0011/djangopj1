from django.shortcuts import render
# Create your views here.
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
# ページへのアクセスをログインユーザーのみに制限する

# Top-view of devolution, select configuration items
class IndexView(generic.TemplateView):
    template_name='index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'message': "Hello World! from View!!",
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        context = {
            'message': "POST method OK!!",
        }
        return render(request, 'index.html', context)

    
