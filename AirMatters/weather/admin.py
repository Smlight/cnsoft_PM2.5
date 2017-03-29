from django.contrib import admin
from weather.models import Beijing, Shanghai, Guangzhou, Shenzhen, Hangzhou, Tianjin, Chengdu, Nanjing, Xian, Wuhan
from weather.models import Realtime, Forecast

# Register your models here.

admin.site.register(Beijing)
admin.site.register(Shanghai)
admin.site.register(Guangzhou)
admin.site.register(Shenzhen)
admin.site.register(Hangzhou)
admin.site.register(Tianjin)
admin.site.register(Chengdu)
admin.site.register(Nanjing)
admin.site.register(Xian)
admin.site.register(Wuhan)

admin.site.register(Realtime)
admin.site.register(Forecast)
