import urllib
import requests
import bs4
import time
import base64
import hashlib
import binascii
import sys

getforecast_url = 'https://free-api.heweather.com/s6/weather?'
getpostion_url = 'https://api.heweather.com/s6/search?parameters'
keyID = ''  #get from heweather.com


def GetWeather(location):
    value = {'location':location, 'key':keyID, 'lang':'zh', 'unit':'m'}
    req = requests.get(getforecast_url, params=value)
    req_json = req.json()
    forecast = req_json['HeWeather6'][0]
    if(forecast['status'] == 'ok'):
        today_weather = forecast['daily_forecast'][0]
        cur_weather = forecast['now']
        res = forecast['update']['loc'] + '\n' + forecast['basic']['admin_area'] + forecast['basic']['location'] + '天气\n' + today_weather['tmp_min'] + '~' + today_weather['tmp_max'] +'℃\n白天' + today_weather['cond_txt_d'] + ', 夜间' + today_weather['cond_txt_n'] + '\n'+  '当前' + cur_weather['cond_txt'] + cur_weather['tmp'] + '℃'
        print("Successfully get weather @" + location)
        return res
    else:
        print("Unsuccessfully get weather @" + location)
        return False

def GetPosition(gps):
    value = {'location':gps, 'key':keyID, 'lang':'zh'}
    req = requests.get(getpostion_url, params = value).json()['HeWeather6'][0]
    if(req['status'] == 'ok'):
        print("Successfully get location information @" + gps)
        return req['basic']
    else:
        print("Unsuccessfully get location information @" + gps)
        return False