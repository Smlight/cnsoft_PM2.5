# -*- encoding:utf-8 -*-
"""AirMatters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from weather.views import redi, tq, tqpred, pm25, pm25pred, login, register, password, noticeWay, suggest

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', redi, name="webroot"),
    url(r'^tq/$', tq, name="tq"),
    url(r'^tqpred/$', tqpred, name="tqpred"),
    url(r'^pm25/$', pm25, name="pm25"),
    url(r'^pm25pred/$', pm25pred, name="pm25pred"),
    url(r'^login/$', login, name="login"),
    url(r'^register/$', register, name="register"),
    url(r'^password/$', password, name="password"),
    url(r'^noticeWay/$', noticeWay, name="noticeWay"),
    url(r'^suggest/$', suggest, name="suggest"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# putting code below is not recommended

import time
from threading import Timer, RLock
from weather.models import Realtime, Forecast
from datetime import datetime, timedelta, tzinfo
import requests

he_key = "88cef94b40a4461ea933dfc44c41f3a2"  # 和风天气API key

CITYS_ID = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'CN101190101', u'Xian': u'CN101110101', u'Wuhan': u'武汉'}

ZERO_TIME_DELTA = timedelta(0)
LOCAL_TIME_DELTA = timedelta(hours=8)  # 本地时区偏差


class LocalTimezone(tzinfo):
    """实现北京时间的类"""

    def utcoffset(self, dt):
        return LOCAL_TIME_DELTA

    def dst(self, dt):
        return ZERO_TIME_DELTA

    def tzname(self, dt):
        return '+08:00'


spl = RLock()


def tq_update():
    cnt = 0
    he_str = "https://free-api.heweather.com/v5/weather"
    for city_str in CITYS_ID:
        payload = {'city': CITYS_ID[city_str], 'key': he_key}
        r = requests.get(he_str, params=payload)
        J = r.json()
        J = J[u"HeWeather5"][0]
        now = Realtime(city=city_str)
        forma = "%Y-%m-%d %H:%M"
        if spl.acquire():
            now.time = datetime.strptime(J[u"basic"][u"update"][u"loc"], forma).replace(tzinfo=LocalTimezone())
            spl.release()
        flag = 0  # no need to update
        try:
            pre = Realtime.objects.filter(city=city_str).earliest("time")
            if pre.time != now.time:
                raise Exception("not eq!")
        except Exception as e:
            print(e)
            flag = 1  # no data before or data too old
        if flag == 1:
            qset = Realtime.objects.filter(city=city_str)
            if qset:
                qset.delete()
            Jnow = J[u"now"]
            now.cond = Jnow[u"cond"][u"txt"]
            now.hum = int(Jnow[u"hum"])
            now.pres = int(Jnow[u"pres"])
            now.pcpn = float(Jnow[u"pcpn"])
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
            Jfores = J[u"hourly_forecast"]
            for Jfore in Jfores:
                fore = Realtime(city=city_str)
                fore.time = datetime.strptime(Jfore[u"date"], forma).replace(tzinfo=LocalTimezone())
                if now.time < fore.time:
                    fore.cond = Jfore[u"cond"][u"txt"]
                    fore.hum = -1
                    fore.pres = -1
                    fore.pcpn = -1
                    fore.tmp = int(Jfore[u"tmp"])
                    fore.vis = -1
                    fore.wind_dir = Jfore[u"wind"][u"dir"]
                    fore.wind_sc = Jfore[u"wind"][u"sc"]
                    fore.aqi = -1
                    fore.pm25 = -1
                    fore.save()
        cnt += 1
        # print cnt, flag
    Timer(600, tq_update).start()


def tqpred_update():
    cnt = 0
    he_str = "https://free-api.heweather.com/v5/forecast"
    for city_str in CITYS_ID:
        payload = {'city': CITYS_ID[city_str], 'key': he_key}
        r = requests.get(he_str, params=payload)
        J = r.json()
        J = J[u"HeWeather5"][0]
        forma = "%Y-%m-%d %H:%M"
        if spl.acquire():
            now_time = datetime.strptime(J[u"basic"][u"update"][u"loc"], forma).replace(tzinfo=LocalTimezone())
            spl.release()
        flag = 0  # no need to update
        try:
            pre_time = Forecast.objects.filter(city=city_str)[0].time
            if pre_time != now_time:
                raise Exception("not eq!")
        except Exception as e:
            print(e)
            flag = 1  # no data before or data too old
        if flag == 1:
            Forecast.objects.filter(city=city_str).delete()
            Jday = J[u"daily_forecast"]
            for Jnow in Jday:
                now = Forecast(city=city_str)
                now.time = now_time
                now.cond = Jnow[u"cond"][u"txt_d"]
                now.date = Jnow[u"date"]
                now.hum = int(Jnow[u"hum"])
                now.pcpn = float(Jnow[u"pcpn"])
                now.pres = int(Jnow[u"pres"])
                now.tmp_max = int(Jnow[u"tmp"][u"max"])
                now.tmp_min = int(Jnow[u"tmp"][u"min"])
                now.vis = int(Jnow[u"vis"])
                now.wind_deg = int(Jnow[u"wind"][u"deg"])
                now.wind_spd = int(Jnow[u"wind"][u"spd"])
                now.save()
        cnt += 1
        # print cnt, flag
    Timer(3600, tq_update).start()


from weather.models import PMBeijing, PMShanghai, PMGuangzhou, PMShenzhen, PMHangzhou, PMTianjin, PMChengdu, PMNanjing, \
    PMXian, PMWuhan

CITYS_UID = {u'Beijing': u'001', u'Shanghai': u'002', u'Guangzhou': u'009', u'Shenzhen': u'004', u'Hangzhou': u'261',
             u'Tianjin': u'006', u'Chengdu': u'008', u'Nanjing': u'050', u'Xian': u'138', u'Wuhan': u'003'}
CITYS_PMDB = {u'Beijing': PMBeijing, u'Shanghai': PMShanghai, u'Guangzhou': PMGuangzhou, u'Shenzhen': PMShenzhen,
              u'Hangzhou': PMHangzhou, u'Tianjin': PMTianjin, u'Chengdu': PMChengdu, u'Nanjing': PMNanjing,
              u'Xian': PMXian, u'Wuhan': PMWuhan}


def pm25_update():
    cnt = 0
    urban_str = "http://urbanair.msra.cn/U_Air/ChangeCity"
    for city_str in CITYS_UID:
        payload = {'CityId': CITYS_UID[city_str], 'Standard': '0'}
        nowdb = CITYS_PMDB[city_str]
        nowdb.objects.all().delete()
        r = requests.get(urban_str, params=payload)
        J = r.json()
        forma = "%m/%d/%Y %I:%M %p"
        if spl.acquire():
            rightTime = datetime.strptime(J[u"UpdateTime"], forma).replace(tzinfo=LocalTimezone())
            spl.release()
        for i in range(len(J[u"CNName"])):
            now = nowdb(station=J[u"CNName"][i])
            now.time = rightTime
            now.timeSlot = 0
            temp = J[u"Stations"][i][u"PM25"]
            if temp:
                now.pm25 = int(temp)
                now.save()
        cnt += 1
        print(cnt)
    Timer(600, pm25_update).start()


def pm25pred_update():
    cnt = 0
    ubpred_str = "http://urbanair.msra.cn/U_Air/GetPredictionV3"

    for city_str in CITYS_UID:
        preddb = CITYS_PMDB[city_str]
        preddb.objects.all().delete()
        for x in range(1, 7):
            payload = {'CityId': CITYS_UID[city_str], 'timeSlot': x, 'Pollutant': 'AQI', 'Standard': '0'}
            r = requests.get(ubpred_str, params=payload)
            J = r.json()
            now_time = datetime.now()
            forma = "%H:%M"
            if spl.acquire():
                rightTime = datetime.strptime(J[u"PredTime"], forma).replace(year=now_time.year, month=now_time.month,
                                                                             day=now_time.day, tzinfo=LocalTimezone())
                # print(rightTime)
                spl.release()
            for i in range(len(J[u"CNName"])):
                pred = preddb(station=J[u"CNName"][i])
                pred.time = rightTime
                pred.timesSlot = x
                temp = J[u"PM25"][i][u"PM25"]
                if temp:
                    pred.pm25 = int(temp)
                    pred.save()
    cnt += 1
    print(cnt)
    Timer(600, pm25pred_update).start()


Timer(0, tq_update).start()
Timer(0, tqpred_update).start()
Timer(0, pm25_update).start()
Timer(0, pm25pred_update).start()
