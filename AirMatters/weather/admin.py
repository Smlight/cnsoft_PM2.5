from django.contrib import admin
from weather.models import PMBeijing, PMShanghai, PMGuangzhou, PMShenzhen, PMHangzhou, PMTianjin, PMChengdu, PMNanjing, \
    PMXian, PMWuhan
from weather.models import Realtime, Forecast

# Register your models here.

admin.site.register(PMBeijing)
admin.site.register(PMShanghai)
admin.site.register(PMGuangzhou)
admin.site.register(PMShenzhen)
admin.site.register(PMHangzhou)
admin.site.register(PMTianjin)
admin.site.register(PMChengdu)
admin.site.register(PMNanjing)
admin.site.register(PMXian)
admin.site.register(PMWuhan)

admin.site.register(Realtime)
admin.site.register(Forecast)
