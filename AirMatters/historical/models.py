from __future__ import unicode_literals

from django.db import models


# Create your models here.
class CityWeather(models.Model):
    date = models.DateField  # 日期
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField  # 湿度
    pcpn = models.FloatField  # 降水量
    pres = models.IntegerField  # 气压
    tmp_max = models.IntegerField  # 最高温度
    tmp_min = models.IntegerField  # 最低温度
    wind_deg = models.IntegerField  # 风向
    wind_spd = models.IntegerField  # 风速

    class Meta:
        abstract = True


class Beijing(CityWeather):  # 北京
    pass


class Shanghai(CityWeather):  # 上海
    pass


class Guangzhou(CityWeather):  # 广州
    pass


class Shenzhen(CityWeather):  # 深圳
    pass


class Hangzhou(CityWeather):  # 杭州
    pass


class Tianjin(CityWeather):  # 天津
    pass


class Chengdu(CityWeather):  # 成都
    pass


class Nanjing(CityWeather):  # 南京
    pass


class Xian(CityWeather):  # 西安
    pass


class Wuhan(CityWeather):  # 武汉
    pass
