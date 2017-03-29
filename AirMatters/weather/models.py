# -*- encoding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models


# 历史天气数据表抽象类
class Daily(models.Model):
    date = models.DateField  # 日期
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField  # 湿度
    pcpn = models.FloatField  # 降水量
    pres = models.IntegerField  # 气压
    tmp_max = models.IntegerField  # 最高温度
    tmp_min = models.IntegerField  # 最低温度
    wind_deg = models.IntegerField  # 风向角度
    wind_spd = models.IntegerField  # 风速
    aqi = models.IntegerField  #
    pm25 = models.IntegerField  #

    class Meta:
        abstract = True


# 每小时天气抽象类
class Hourly(models.Model):
    city = models.CharField(max_length=30)  #
    datetime = models.DateTimeField  #
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField  # 湿度
    pcpn = models.FloatField  # 降水量
    pres = models.IntegerField  # 气压
    tmp_max = models.IntegerField  # 最高温度
    tmp_min = models.IntegerField  # 最低温度
    wind_dir = models.CharField(max_length=30)  # 风向描述
    wind_spd = models.IntegerField  # 风速
    aqi = models.IntegerField  #
    pm25 = models.IntegerField  #
    suggestion = models.CharField(max_length=3000)  #

    class Meta:
        abstract = True


class Realtime(Hourly):
    pass


class Forecast(Hourly):
    pass


# 历史天气具体类，共十个城市
class Beijing(Daily):  # 北京
    pass


class Shanghai(Daily):  # 上海
    pass


class Guangzhou(Daily):  # 广州
    pass


class Shenzhen(Daily):  # 深圳
    pass


class Hangzhou(Daily):  # 杭州
    pass


class Tianjin(Daily):  # 天津
    pass


class Chengdu(Daily):  # 成都
    pass


class Nanjing(Daily):  # 南京
    pass


class Xian(Daily):  # 西安
    pass


class Wuhan(Daily):  # 武汉
    pass
