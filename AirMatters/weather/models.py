# -*- encoding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models


# 每日天气数据表抽象类
class Daily(models.Model):
    date = models.DateField()  # 日期
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField()  # 湿度
    pcpn = models.FloatField()  # 降水量
    pres = models.IntegerField()  # 气压
    tmp_max = models.IntegerField()  # 最高温度
    tmp_min = models.IntegerField()  # 最低温度
    vis = models.IntegerField()  # 能见度
    wind_deg = models.IntegerField()  # 风向角度
    wind_spd = models.IntegerField()  # 风速
    aqi = models.IntegerField()  # 空气质量
    pm25 = models.IntegerField()  #

    class Meta:
        abstract = True


# 监测站每小时PM2.5抽象类
class HPM25(models.Model):
    station = models.CharField(max_length=30)  # 监测站
    time = models.DateTimeField()  # 时间
    pm25 = models.IntegerField()  #

    class Meta:
        abstract = True


class PMRealtime(HPM25):
    pass


# PM2.5天气具体类，共十个城市
class PMBeijing(HPM25):  # 北京
    pass


class PMShanghai(HPM25):  # 上海
    pass


class PMGuangzhou(HPM25):  # 广州
    pass


class PMShenzhen(HPM25):  # 深圳
    pass


class PMHangzhou(HPM25):  # 杭州
    pass


class PMTianjin(HPM25):  # 天津
    pass


class PMChengdu(HPM25):  # 成都
    pass


class PMNanjing(HPM25):  # 南京
    pass


class PMXian(HPM25):  # 西安
    pass


class PMWuhan(HPM25):  # 武汉
    pass


# 每小时天气抽象类
class Hourly(models.Model):
    city = models.CharField(max_length=30)  # 城市
    time = models.DateTimeField()  # 时间
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField()  # 湿度
    pres = models.IntegerField()  # 气压
    tmp = models.IntegerField()  # 温度
    vis = models.IntegerField()  # 能见度
    wind_dir = models.CharField(max_length=30)  # 风向描述
    wind_sc = models.CharField(max_length=30)  # 风强
    aqi = models.IntegerField()  # 空气质量
    aqi_str = models.CharField(max_length=30)  # 空气质量描述
    pm25 = models.IntegerField()  #
    suggestion = models.CharField(max_length=3000)  # 生活建议

    class Meta:
        abstract = True


class Realtime(Hourly):
    pass


class Forecast(Hourly):
    pass
