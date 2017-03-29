# -*- encoding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from weather.models import Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Tianjin, Chengdu, Nanjing, Xian, Wuhan
from weather.models import Realtime, Forecast
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})


def hello(request):
    return HttpResponse(
        r'<iframe allowtransparency="true" frameborder="0" width="600" height="98" scrolling="no" src="//tianqi.2345.com/plugin/widget/index.htm?s=2&z=3&t=1&v=0&d=3&bd=0&k=&f=&q=1&e=1&a=1&c=54511&w=600&h=98&align=center"></iframe>')


import requests

he_key = "88cef94b40a4461ea933dfc44c41f3a2"  # 和风天气API key
he_str = "https://free-api.heweather.com/v5/weather"  # 和风天气API 接口


def default(request):
    city_str = 'beijing'
    pre = Realtime.objects.get(city=city_str)
    now = pre
    if pre.datetime + datetime.timedelta(hours=1) < datetime.datetime.now():
        pre.delete()
        payload = {'city': city_str, 'key': he_key}
        r = requests.get(he_str, params=payload)
        M = r.json()
        M = M[u'HeWeather5'][0]

    webmain = r.text
    return render(request, 'realtime.html', {'webmain': webmain})
