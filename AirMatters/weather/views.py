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
    try:
        pre = Realtime.objects.get(city=city_str)
    except:
        pre = Realtime(city=city_str)
        pre.time = datetime.datetime.now() + datetime.timedelta(hours=-2)
    now = pre
    webmain = str(datetime.datetime.now())
    if pre.time + datetime.timedelta(hours=1) < datetime.datetime.now():
        if pre.id:
            pre.delete()
        payload = {'city': city_str, 'key': he_key}
        # try:

        r = requests.get(he_str, params=payload)
        J = r.json()
        J = J[u'HeWeather5'][0]
        if J[u'status'] != u'ok':
            pass
        now = Realtime(city=city_str)
        now.time = J[u'basic'][u'update'][u'loc']
        Jnow = J[u'now']
        now.cond = Jnow[u'cond'][u'txt']
        now.hum = int(Jnow[u'hum'])
        now.pcpn = int(Jnow[u'pcpn'])
        now.pres = int(Jnow[u'pres'])
        now.tmp = int(Jnow[u'tmp'])
        now.vis = int(Jnow[u'vis'])
        now.wind_dir = Jnow[u'wind'][u'dir']
        now.wind_sc = Jnow[u'wind'][u'sc']
        Jaqi = J[u'aqi'][u'city']
        now.aqi = int(Jaqi[u'aqi'])
        now.aqi_str = Jaqi[u'qlty']
        now.pm25 = int(Jaqi[u'pm25'])
        now.suggestion = J[u'suggestion']
        now.save()
        webmain = str(J)

        # except:
        #     webmain = u'NetWork FatalError!'

    return render(request, 'realtime.html', {'webmain': webmain, 'now': now})
