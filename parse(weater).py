import requests
import json
from datetime import datetime

API_key = 'b47d9ec1405359d146e41bd7c750adae'
city_name = 'Cherkessk'
country = 'RU'
lat = 44.2233
lon = 42.0578
exclude = 'minutely,hourly,alerts'

URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}'
r = requests.get(URL)
weater = r.json()
daily = weater['daily']


def to_cels(temp):
    t = temp - 273.15
    return t


def get_temps(daily):
    dif_temps = []
    for i in daily:
        d_temp = abs(round(to_cels(i['temp'].get('morn')) - to_cels(i['temp'].get('night')), 2))
        dif_temps.append(d_temp)
    return dif_temps


def get_pressure(daily):
    pressures = []
    for i in range(5):
        pressures.append(daily[i].get('pressure'))
    return pressures


def get_day(daily, dif_temps):
    for i in daily:
        t = round(abs(i['temp'].get('morn') - i['temp'].get('night')), 2)
        if t == max(dif_temps):
            d = datetime.fromtimestamp(i.get('dt')).date()
    return d, t


dif_temps = get_temps(daily)
max_pres = max(get_pressure(daily))
print('Максимальное давление за 5 дней: ', max_pres)
day, temp = get_day(daily, dif_temps)
print('День с максимальной разницей: ', day)
print('Разница температур: ', temp)
