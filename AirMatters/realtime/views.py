from django.shortcuts import render

# Create your views here.

he_key = "88cef94b40a4461ea933dfc44c41f3a2"  # 和风天气API key
he_str = "https://free-api.heweather.com/v5/weather?city=%s&key=%s"  # 和风天气API 接口


def realtime(request):
    query_str = he_str % ('beijing', he_key)
    res_str = ''
    return render(request, 'realtime.html', {'webmain': res_str})
