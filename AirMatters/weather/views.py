# -*- encoding:utf-8 -*-

from django.shortcuts import render
# from weather.models import Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Tianjin, Chengdu, Nanjing, Xian, Wuhan
from weather.models import PMBeijing, PMShanghai, PMGuangzhou, PMShenzhen, PMHangzhou, PMTianjin, PMChengdu, PMNanjing, \
    PMXian, PMWuhan
from weather.models import Realtime, Forecast
from weather.models import UserProfile

# CITYS_DB = {u'Beijing': Beijing, u'Shanghai': Shanghai, u'Guangzhou': Guangzhou, u'Shenzhen': Shenzhen,
#             u'Hangzhou': Hangzhou, u'Tianjin': Tianjin, u'Chengdu': Chengdu, u'Nanjing': Nanjing, u'Xian': Xian,
#             u'Wuhan': Wuhan}

import requests
import time

CITYS_CN = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'南京', u'Xian': u'西安', u'Wuhan': u'武汉'}
CITYS_ID = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'CN101190101', u'Xian': u'CN101110101', u'Wuhan': u'武汉'}

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext


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
    city_note = CITYS_CN[city_str]
    try:
        qset = Realtime.objects.filter(city=city_str)
        now = qset[0]
        J = eval(str(now.suggestion))
        LABELS_CN = {u"comf": u"舒适指数", u"cw": u"洗车建议", u"drsg": u"穿衣建议", u"flu": u"感冒指数", u"sport": u"运动建议",
                     u"trav": u"旅游建议", u"uv": u"紫外线指数", u"air": u"空气指数"}
        suggest = {}
        for x in J:
            suggest[LABELS_CN[x]] = [J[x][u"brf"], J[x][u"txt"]]
        llist = []
        dlist = []
        try:
            llist.append(qset[1].time.hour)
            dlist.append(qset[1].tmp)
            for row in qset[2:]:
                ltmp = llist[-1]
                dtmp = dlist[-1]
                llist.append(ltmp + 1)
                dlist.append(dtmp * 2.0 / 3 + row.tmp * 1.0 / 3)
                llist.append(ltmp + 2)
                dlist.append(dtmp * 1.0 / 3 + row.tmp * 2.0 / 3)
                llist.append(row.time.hour)
                dlist.append(row.tmp)
            llist = [str((x + 8) % 24) + u'时' for x in llist]
            dlist = [round(x, 0) for x in dlist]
            tmax, tmin = max(dlist), min(dlist)
            tmp = max(int((tmax - tmin) / 3.0 + 0.5), 1)
            tmax, tmin = tmax + tmp, tmin - tmp
        except Exception as e:
            pass
        return render(request, 'tq.html', {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note,
                                           'now': now, 'llsit': llist, 'dlist': dlist, 'tmax': tmax,
                                           'tmin': tmin, 'suggest': suggest})
    except Exception as e:
        print(e)
        return render(request, 'tq.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


def tqpred(request):
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = CITYS_CN[city_str]
    try:
        qset = Forecast.objects.filter(city=city_str)
        l = []
        up_time = None
        for r in qset:
            if not up_time:
                up_time = r.time
            l.append(r)
        return render(request, 'tqpred.html',
                      {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note, 'time': up_time, 'list': l})
    except Exception as e:
        print(e)
        return render(request, 'tq.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


urban_str = "http://urbanair.msra.cn/U_Air/ChangeCity"
CITYS_UID = {u'Beijing': u'001', u'Shanghai': u'002', u'Guangzhou': u'009', u'Shenzhen': u'004', u'Hangzhou': u'261',
             u'Tianjin': u'006', u'Chengdu': u'008', u'Nanjing': u'050', u'Xian': u'138', u'Wuhan': u'003'}
CITYS_PMDB = {u'Beijing': PMBeijing, u'Shanghai': PMShanghai, u'Guangzhou': PMGuangzhou, u'Shenzhen': PMShenzhen,
              u'Hangzhou': PMHangzhou, u'Tianjin': PMTianjin, u'Chengdu': PMChengdu, u'Nanjing': PMNanjing,
              u'Xian': PMXian, u'Wuhan': PMWuhan}


def pm25(request):
    "Realtime pm2.5 information and hourly forecast"
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = CITYS_CN[city_str]
    try:
        nowdb = CITYS_PMDB[city_str]
        now = Realtime.objects.filter(city=city_str).earliest("time")
        rightTime = nowdb.objects.earliest("time").time
        qset = nowdb.objects.filter(timeSlot=0)
        l = []
        for r in qset:
            l.append(r)
        return render(request, 'pm25.html',
                      {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note, 'now': now,
                       'time': rightTime, 'list': l})
    except Exception as e:
        print(e)
        return render(request, 'pm25.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


def pm25pred(request):
    city_str = request.GET.get('city')
    ncity_str = city_dete(city_str)
    if city_str != ncity_str:
        return HttpResponseRedirect(request.path + '?city=' + ncity_str)
    city_note = CITYS_CN[city_str]
    try:
        preddb = CITYS_PMDB[city_str]
        qset = preddb.objects.all()
        tab = {}
        up_time = None
        for r in qset:
            if not up_time:
                up_time = r.time
            if not tab.get(r.station):
                tab[r.station] = []
            tab.setdefault(r.station, []).append(r.pm25)
        return render(request, 'pm25pred.html',
                      {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note, 'time': up_time,
                       'dict': tab})
    except Exception as e:
        print(e)
        return render(request, 'pm25pred.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


def userlogin(request):
    if request.method == "post":
        username = request.POST.get("userName")
        userpwd = request.POST.get("userPwd")
        user = authenticate(username=username, password=userpwd)
        if user:
            login(request, user)
            return redirect('/noticeWay.html')
    return render(request, 'login.html')


def userlogout(request):
    logout(request)
    return render(request, 'login.html')


def register(request):
    errors = []
    try:
        if request.method == 'POST':
            username = request.POST.get('userName', '')
            userpwd = request.POST.get('userPwd', '')
            userpwd2 = request.POST.get('userPwd2', '')
            userEmail = request.POST.get('userEmail', '')
            userPhone = request.POST.get('userPhone', '')
            notice = request.POST.get('noNotice', '')
            byPhone = request.POST.get('byPhone', '')
            byEmail = request.POST.get('byEmail', '')
            if userpwd != userpwd2:
                errors.append("两次输入的密码不一致!")
                return render_to_response("register.html", RequestContext(request,
                                                                          {'username': username, 'userEmail': userEmail,
                                                                           'errors': errors}))
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                errors.append("用户名已存在")
                return render_to_response("register.html", RequestContext(request,
                                                                          {'username': username, 'userEmail': userEmail,
                                                                           'errors': errors}))
            user = User()
            user.username = username
            user.set_password(userpwd)
            user.email = userEmail
            user.save()

            profile = UserProfile()
            profile.user_id = user.id
            profile.phone = userPhone
            profile.noNotice = notice
            profile.byPhone = byPhone
            profile.byEmail = byEmail
            profile.save()
    except Exception as e:
        errors.append(str(e))
        return render_to_response("register.html", RequestContext(request, {'errors': errors}))
    return render(request, 'register.html')


def password(request):
    return render(request, 'password.html')


def noticeWay(request):
    return render(request, 'noticeWay.html')


def suggest(request):
    return render(request, 'suggest.html')
