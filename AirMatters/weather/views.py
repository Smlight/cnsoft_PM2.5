# -*- encoding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from weather.models import Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Tianjin, Chengdu, Nanjing, Xian, Wuhan
from weather.models import Realtime, Forecast


def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'pm25.html', {'current_date': now})


def hello(request):
    return HttpResponse(
        r'<iframe allowtransparency="true" frameborder="0" width="600" height="98" scrolling="no" src="//tianqi.2345.com/plugin/widget/index.htm?s=2&z=3&t=1&v=0&d=3&bd=0&k=&f=&q=1&e=1&a=1&c=54511&w=600&h=98&align=center"></iframe>')


import requests

he_key = "88cef94b40a4461ea933dfc44c41f3a2"  # 和风天气API key
he_str = "https://free-api.heweather.com/v5/weather"  # 和风天气API 接口

from datetime import datetime, timedelta
from django.utils import timezone

CITYS_CN = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'南京', u'Xian': u'西安', u'Wuhan': u'武汉'}


def deteCity(city_str):
    city_str = city_str.capitalize()
    if not city_str:
        city_str = 'Beijing'
        city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])
    else:
        if city_str[-1] == '/':
            city_str = city_str[:-1:]
        if city_str not in CITYS_CN:
            city_str = 'Beijing'
            city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])
        else:
            city_note = u'当前城市：%s' % (CITYS_CN[city_str])
    return city_str, city_note


def tianqi(request, city_str):
    "Realtime weather information and hourly forecast"
    # HTTP requests in this function should be changed into asynchronous operation
    city_str, city_note = deteCity(city_str)
    flag = 0  # no need to update
    try:
        pre = Realtime.objects.get(city=city_str)
    except:
        flag = 1  # no data before
    if flag == 0 and pre.time + timedelta(hours=1) < timezone.now():
        pre.delete()
        flag = 2  # data too old

    status_note = u'OK'
    if flag == 0:
        now = pre
    else:
        try:
            payload = {'city': CITYS_CN[city_str], 'key': he_key}
            r = requests.get(he_str, params=payload)
            J = r.json()
            J = J[u"HeWeather5"][0]
            if J[u"status"] != u"ok":
                raise Exception("Not OK!")
            now = Realtime(city=city_str)
            now.time = J[u"basic"][u"update"][u"loc"]
            Jnow = J[u"now"]
            now.cond = Jnow[u"cond"][u"txt"]
            now.hum = int(Jnow[u"hum"])
            now.pres = int(Jnow[u"pres"])
            now.tmp = int(Jnow[u"tmp"])
            now.vis = int(Jnow[u"vis"])
            now.wind_dir = Jnow[u"wind"][u"dir"]
            now.wind_sc = Jnow[u"wind"][u"sc"]
            Jaqi = J[u"aqi"][u"city"]
            now.aqi = int(Jaqi[u"aqi"])
            now.aqi_str = Jaqi[u"qlty"]
            now.pm25 = int(Jaqi[u"pm25"])
            now.suggestion = J[u"suggestion"]
            now.save()
        except requests.ConnectionError:
            status_note = u'网络连接错误，请重试'
        except "Not OK!":
            status_note = u'天气服务器错误，请重试'
        except Exception, e:
            status_note = str(e) + u'       内部错误，请联系管理员'
    if status_note == u'OK':
        J = eval(str(now.suggestion))
        LABELS_CN = {u"comf": u"舒适指数", u"cw": u"洗车建议", u"drsg": u"穿衣建议", u"flu": u"感冒指数", u"sport": u"运动建议",
                     u"trav": u"旅游建议", u"uv": u"紫外线指数", u"air": u"空气指数"}
        suggest = u""
        for x in J:
            suggest += u"%s：%s\n%s\n\n" % (LABELS_CN[x], J[x][u"brf"], J[x][u"txt"])
        return render(request, 'tianqi.html',
                      {'status_note': status_note, 'city_note': city_note, 'now': now, 'suggest': suggest})
    else:
        return render(request, 'tianqi.html', {'status_note': status_note})


urban_str = "http://urbanair.msra.cn/U_Air/ChangeCity"
CITYS_UID = {u'Beijing': u'001', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
             u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'050', u'Xian': u'西安', u'Wuhan': u'武汉'}


def pm25(request, city_str):
    "Realtime pm2.5 information and hourly forecast"
    # HTTP requests in this function should be changed into asynchronous operation
    city_str, city_note = deteCity(city_str)
    payload = {'CityId': CITYS_UID[city_str], 'Standard': '0'}
    r = requests.get(urban_str, params=payload)
    return render(request, 'pm25.html', {'city_note': city_note, 'main': r.text})
