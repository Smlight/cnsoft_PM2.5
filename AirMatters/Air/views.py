from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hello(request):
    return HttpResponse(r'<iframe allowtransparency="true" frameborder="0" width="600" height="98" scrolling="no" src="//tianqi.2345.com/plugin/widget/index.htm?s=2&z=3&t=1&v=0&d=3&bd=0&k=&f=&q=1&e=1&a=1&c=54511&w=600&h=98&align=center"></iframe>')