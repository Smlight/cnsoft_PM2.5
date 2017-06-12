# -*- encoding:utf-8 -*-

from weather.models import PMBeijing, PMShanghai, PMGuangzhou, PMShenzhen, PMHangzhou, PMTianjin, PMChengdu, PMNanjing, \
    PMXian, PMWuhan
from weather.models import Realtime, Forecast
from weather.models import UserProfile

CITYS_CN = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'南京', u'Xian': u'西安', u'Wuhan': u'武汉'}
CITYS_ID = {u'Beijing': u'北京', u'Shanghai': u'上海', u'Guangzhou': u'广州', u'Shenzhen': u'深圳', u'Hangzhou': u'杭州',
            u'Tianjin': u'天津', u'Chengdu': u'成都', u'Nanjing': u'CN101190101', u'Xian': u'CN101110101', u'Wuhan': u'武汉'}

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
import re


def city_dete(city_str):
    if city_str and city_str.capitalize() in CITYS_CN:
        city_str = city_str.capitalize()
    else:
        city_str = 'Beijing'
    return city_str


def redi(request):
    # auto city detected shall be added
    if request.user.is_authenticated():
        query = UserProfile.objects.get(user=request.user)
        request.session['city'] = query.userCity
        return HttpResponseRedirect('/tq')
    else:
        request.session['city'] = 'Beijing'
        return HttpResponseRedirect('/tq')


def tq(request):
    "Realtime weather information and hourly forecast"
    city_str = request.GET.get('city')
    if city_str is None:
        city_str = request.session['city']
    else:
        ncity_str = city_dete(city_str)
        if city_str != ncity_str:
            request.session['city'] = ncity_str
            return HttpResponseRedirect(request.path)
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
    if city_str is None:
        city_str = request.session['city']
    else:
        ncity_str = city_dete(city_str)
        if city_str != ncity_str:
            request.session['city'] = ncity_str
            return HttpResponseRedirect(request.path)
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
    if city_str is None:
        city_str = request.session['city']
    else:
        ncity_str = city_dete(city_str)
        if city_str != ncity_str:
            request.session['city'] = ncity_str
            return HttpResponseRedirect(request.path)
    city_note = CITYS_CN[city_str]
    try:
        llist = []
        dlist = []
        for k, v in CITYS_CN.items():
            now = Realtime.objects.filter(city=k).earliest("time")
            llist.append(v)
            dlist.append(now.pm25)
        return render(request, 'pm25.html',
                      {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note, 'llist': llist,
                       'dlist': dlist})
    except Exception as e:
        print(e)
        return render(request, 'pm25.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


def pm25pred(request):
    city_str = request.GET.get('city')
    if city_str is None:
        city_str = request.session['city']
    else:
        ncity_str = city_dete(city_str)
        if city_str != ncity_str:
            request.session['city'] = ncity_str
            return HttpResponseRedirect(request.path)
    city_note = CITYS_CN[city_str]
    try:
        preddb = CITYS_PMDB[city_str]
        qset = preddb.objects.filter(timeSlot=0)
        tab = {}
        up_time = None
        for i in qset:
            tab[i.station] = []
            if not up_time:
                up_time = i.time
            tab.setdefault(i.station, []).append(i.pm25)
        for i in range(1, 7):
            for k in tab:
                q = preddb.objects.filter(station=k, timeSlot=i)
                if q:
                    if not up_time:
                        up_time = q.time
                    # tab[k].append(q.pm25)
                    tab.setdefault(k, []).append(q[0].pm25)
                else:
                    tab.setdefault(k, []).append("—")
        return render(request, 'pm25pred.html',
                      {'status_note': u"OK", 'city_str': city_str, 'city_note': city_note, 'time': up_time,
                       'dict': tab})
    except Exception as e:
        print(e)
        return render(request, 'pm25pred.html', {'status_note': u"BAD", 'city_str': city_str, 'city_note': city_note})


def userlogin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get("userName")
            userpwd = request.POST.get("userPwd")
            user = authenticate(username=username, password=userpwd)
            if user is not None:
                login(request, user)
            else:
                raise Exception('账号密码有误')
        except Exception as e:
            print(e)
            return render(request, 'error.html', {'data': e})
        return render(request, 'error.html', {'data': 'OK'})
    else:
        return Http404


def userlogout(request):
    logout(request)
    return render(request, 'error.html', {'data': 'OK'})


def checkregi(username, userpwd, userpwd2, userEmail, userPhone):
    try:
        qres = User.objects.get(username=username)
        raise Exception('用户名已存在')
    except ObjectDoesNotExist as e:
        if username == '':
            raise Exception('用户名为空')
        if userpwd == '':
            raise Exception('密码为空')
        if userpwd != userpwd2:
            raise Exception('两次输入的密码不一致')
        if re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',
                    userEmail) is None:
            raise Exception('您的邮箱输入有误')
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch = p.match(userPhone)
        if phonematch is None:
            raise Exception('您的电话有误')
        return username


@csrf_protect
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('userName', '')
            userpwd = request.POST.get('userPwd', '')
            userpwd2 = request.POST.get('userPwd2', '')
            userEmail = request.POST.get('userEmail', '')
            userPhone = request.POST.get('userPhone', '')
            notice = request.POST.get('noNotice', '')
            byPhone = request.POST.get('byPhone', '')
            byEmail = request.POST.get('byEmail', '')
            userCity = request.POST.get('userCity', '')
            username = checkregi(username, userpwd, userpwd2, userEmail, userPhone)

            user = User()
            user.username = username
            user.set_password(userpwd)
            user.email = userEmail
            user.save()
            profile = UserProfile.objects.get(user_id=user.id)
            profile.phone = userPhone
            profile.userCity = userCity
            if notice != "on":
                if byPhone != "on":
                    profile.byPhone = False
                else:
                    profile.byPhone = True
                if byEmail != "on":
                    profile.byEmail = False
                else:
                    profile.byEmail = True
            else:
                profile.noNotice = True
            profile.save()
        except Exception as e:
            print(e)
            return render(request, 'error.html', {'data': e})
        return userlogin(request)
    else:
        return Http404


def password(request):
    query = UserProfile.objects.get(user=request.user)
    city_str = query.userCity
    city_note = CITYS_CN[city_str]
    if request.method == 'POST':
        try:
            username = request.user.username
            oldPwd = request.POST.get('userPwd')
            newPwd1 = request.POST.get('userNewPwd')
            newPwd2 = request.POST.get('userNewPwd2')
            user = authenticate(username=username, password=oldPwd)
            if user:
                if newPwd1 == newPwd2:
                    if oldPwd == newPwd1:
                        raise Exception('新密码与原密码相同')
                    u = User.objects.get(username=username)
                    u.set_password(newPwd1)
                    u.save()
                    tmp_c = request.session['city']
                    logout(request)
                    user = authenticate(username=username, password=newPwd1)
                    login(request, user)
                    request.session['city'] = tmp_c
                else:
                    raise Exception('两次输入的新密码不一致')
            else:
                raise Exception('原密码错误')
        except Exception as e:
            print(e)
            return render(request, 'error.html', {'data': e})
        return render(request, 'error.html', {'data': 'OK'})
    else:
        return render(request, 'password.html', {'city_str': city_str, 'city_note': city_note})


def noticeWay(request):
    if request.method == 'POST':
        try:
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            notice = request.POST.get('noNotice')
            byPhone = request.POST.get('byPhone')
            byEmail = request.POST.get('byEmail')
            userCity = request.POST.get('userCity')
            print(request.user.userprofile.byEmail)
            if re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',
                        email) is None:
                raise Exception('您的邮箱输入有误')
            p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
            phonematch = p.match(phone)
            if phonematch is None:
                raise Exception('您的电话有误')
            username = request.user.username
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user_id=user.id)
            profile.userCity = userCity
            request.session['city'] = userCity
            if phone:
                profile.phone = phone
            if email:
                user.email = email
            if notice == 'on':
                profile.noNotice = True
                profile.byEmail = False
                profile.byPhone = False
            else:
                if byEmail:
                    profile.byEmail = True
                if byPhone:
                    profile.byPhone = True
            user.save()
            profile.save()
        except Exception as e:
            print(e)
            return render(request, 'error.html', {'data': e})
        return render(request, 'error.html', {'data': '更新成功！'})
    else:
        return Http404


def suggest(request):
    return render(request, 'suggest.html')
