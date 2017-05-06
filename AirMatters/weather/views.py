# -*- encoding:utf-8 -*-

# Create your views here.

from django.shortcuts import render
# from weather.models import Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Tianjin, Chengdu, Nanjing, Xian, Wuhan
from weather.models import PMBeijing, PMShanghai, PMGuangzhou, PMShenzhen, PMHangzhou, PMTianjin, PMChengdu, PMNanjing, \
    PMXian, PMWuhan
from weather.models import Realtime, Forecast

# CITYS_DB = {u'Beijing': Beijing, u'Shanghai': Shanghai, u'Guangzhou': Guangzhou, u'Shenzhen': Shenzhen,
#             u'Hangzhou': Hangzhou, u'Tianjin': Tianjin, u'Chengdu': Chengdu, u'Nanjing': Nanjing, u'Xian': Xian,
#             u'Wuhan': Wuhan}

import requests
import time

he_key = "88cef94b40a4461ea933dfc44c41f3a2"  # 和风天气API key
he_str = "https://free-api.heweather.com/v5/weather"  # 和风天气API 接口

from datetime import datetime, timedelta
from django.utils import timezone

CITYS_CN = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'南京', u'Xian': u'西安', u'Wuhan': u'武汉'}
CITYS_ID = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'CN101190101', u'Xian': u'CN101110101', u'Wuhan': u'武汉'}

from django.http import HttpResponseRedirect


def city_dete(city_str):
    if city_str and city_str.capitalize() in CITYS_CN:
        city_str = city_str.capitalize()
    else:
        city_str = 'Beijing'
    return city_str


def redi(request):
    # auto city detected shall be added
    return HttpResponseRedirect('/tq/')


def tq(request):
    "Realtime weather information and hourly forecast"
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])

    try:
        now = Realtime.objects.get(city=city_str)
        J = eval(str(now.suggestion))
        LABELS_CN = {u"comf": u"舒适指数", u"cw": u"洗车建议", u"drsg": u"穿衣建议", u"flu": u"感冒指数", u"sport": u"运动建议",
                     u"trav": u"旅游建议", u"uv": u"紫外线指数", u"air": u"空气指数"}
        suggest = {}
        for x in J:
            suggest[LABELS_CN[x]] = [J[x][u"brf"], J[x][u"txt"]]
        return render(request, 'tq.html', {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note,
                                           'now': Realtime.objects.get(city=city_str), 'suggest': suggest})
    except Exception, e:
        print e
        return render(request, 'tq.html', {'status_note': u"BAD", 'city_str': city_str})


def tqpred(request):
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])
    return render(request, 'tqpred.html', {'city_str': city_str, 'city_note': city_note})


urban_str = "http://urbanair.msra.cn/U_Air/ChangeCity"
CITYS_UID = {u'Beijing': u'001', u'Shanghai': u'002', u'Guangzhou': u'009', u'Shenzhen': u'004', u'Hangzhou': u'261',
             u'Tianjin': u'006', u'Chengdu': u'008', u'Nanjing': u'050', u'Xian': u'138', u'Wuhan': u'003'}

CITYS_PMDB = {u'Beijing': PMBeijing, u'Shanghai': PMShanghai, u'Guangzhou': PMGuangzhou, u'Shenzhen': PMShenzhen,
              u'Hangzhou': PMHangzhou, u'Tianjin': PMTianjin, u'Chengdu': PMChengdu, u'Nanjing': PMNanjing,
              u'Xian': PMXian, u'Wuhan': PMWuhan}


def pm25(request):
    "Realtime pm2.5 information and hourly forecast"
    # HTTP requests in this function should be changed into asynchronous operation
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])
    payload = {'CityId': CITYS_UID[city_str], 'Standard': '0'}
    nowdb = CITYS_PMDB[city_str]
    r = requests.get(urban_str, params=payload)
    J = r.json()
    a = J[u"UpdateTime"]
    timeArray = time.strptime(a, "%m/%d/%Y %I:%M %p")
    rightTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    l = []
    for i in range(len(J[u"CNName"])):
        now = nowdb(station=J[u"CNName"][i])
        now.time = rightTime
        temp = J[u"Stations"][i][u"PM25"]
        if temp is None:
            now.pm25 = -1
        else:
            now.pm25 = int(temp)
        l.append(now)
        now.save()
    return render(request, 'pm25.html', {'city_str': city_str, 'city_note': city_note, 'time': rightTime, 'list': l})


ubpred_str = "http://urbanair.msra.cn/U_Air/GetPredictionV3"


def pm25pred(request):
    # HTTP requests in this function should be changed into asynchronous operation
    # global pred
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = u'城市已设定为：%s' % (CITYS_CN[city_str])
    payload = {'CityId': CITYS_UID[city_str], 'timeSlot': '1', 'Pollutant': 'AQI', 'Standard': '0'}
    preddb = CITYS_PMDB[city_str]
    r = requests.get(ubpred_str, params=payload)
    J = r.json()
    a = J[u"PredTime"]
    data = datetime.now().strftime('%Y-%m-%d')
    data = data + " " + a
    timeArray = time.strptime(data, "%Y-%m-%d %H:%M")
    rightTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    l = []
    for i in range(len(J[u"CNName"])):
        pred = preddb(station=J[u"CNName"][i])
        pred.time = rightTime
        temp = J[u"PM25"][i][u"PM25"]
        if temp == "null":
            pred.pm25 = -1
        else:
            pred.pm25 = int(temp)
        l.append(pred)
        pred.save()
    return render(request, 'pm25pred.html',
                  {'city_str': city_str, 'city_note': city_note, 'time': rightTime, 'list': l})


def login(request):
    pass


def register(request):
    pass
