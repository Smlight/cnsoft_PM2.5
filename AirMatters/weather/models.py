from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# 城市每小时PM2.5抽象类
class CHPM25(models.Model):
    time = models.DateTimeField()  # 时间
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField()  # 湿度
    vis = models.IntegerField()  # 能见度
    wind_dir = models.CharField(max_length=30)  # 风向描述
    wind_spd = models.IntegerField()  # 风速
    aqi = models.IntegerField()  # 空气质量
    aqi_str = models.CharField(max_length=30)  # 空气质量描述
    pm25 = models.IntegerField()  #

    class Meta:
        abstract = True


# 监测站每小时PM2.5抽象类
class HPM25(models.Model):
    station = models.CharField(max_length=30)  # 监测站
    time = models.DateTimeField()  # 时间
    timeSlot = models.IntegerField()  # 预测时间节点
    pm25 = models.IntegerField()  #

    class Meta:
        abstract = True


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
    vis = models.IntegerField()  # 能见度(km)
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


# 每日天气数据表抽象类
class Daily(models.Model):
    city = models.CharField(max_length=30)  # 城市
    time = models.DateTimeField()  # 更新时间
    date = models.DateField()  # 日期
    cond = models.CharField(max_length=30)  # 天气情况
    hum = models.IntegerField()  # 湿度
    pcpn = models.FloatField()  # 降水量
    pres = models.IntegerField()  # 气压
    tmp_max = models.IntegerField()  # 最高温度
    tmp_min = models.IntegerField()  # 最低温度
    vis = models.IntegerField()  # 能见度(km)
    wind_deg = models.IntegerField()  # 风向角度
    wind_spd = models.IntegerField()  # 风速

    class Meta:
        abstract = True


class Forecast(Daily):
    pass


# 用户扩展类
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20, default='0')
    noNotice = models.BooleanField(default=False)
    byPhone = models.BooleanField(default=False)
    byEmail = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)


