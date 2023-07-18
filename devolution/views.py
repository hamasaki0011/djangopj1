from django.shortcuts import render
# Create your views here.
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

# Top-view of devolution, select configuration items
#@csrf_exempt
class DevolutionIndexView(generic.TemplateView):
    template_name='devolution/devolution_index.html'

    #@csrf_exempt
    def get(self, request, *args, **kwargs):
        context = {
            'message': "Hello World! from View!!",
        }
        return render(request, 'devolution/devolution_index.html', context)

    def post(self, request, *args, **kwargs):
        context = {
            'message': "POST method OK!!",
        }
        return render(request, 'devolution/devolution_index.html', context)

    
