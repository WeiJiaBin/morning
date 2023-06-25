from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
my_user_id = os.environ["MY_USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
HE_FENG_KEY = os.environ["HE_FENG_KEY"]

def get_weather():

    hefeng_key = HE_FENG_KEY
    location = '101190107'
    url = "https://devapi.qweather.com/v7/weather/now?key=" + hefeng_key + "&location=" + location
    res = requests.get(url).json()
    weather = res['now']
    weather['text'] = city + "-" + weather['text']
    return weather['text'], weather['feelsLike']

def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
get_words_text = get_words()
random_color = get_random_color()
# wea, temperature = "小宝宝", "520"
data = {"weather": {"value": wea}, "temperature": {"value": temperature}, "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()}, "words": {"value": get_words_text, "color": random_color}}
res = wm.send_template(user_id, template_id, data)
res2 = wm.send_template(my_user_id, template_id, data)
print(res)
print(res2)
template_id2 = "BW6sZBjGCVxZ4n648OPYD6nqYDEViMHAMCQTBhX-6y0"
data2 = {"words":{"value":get_words_text, "color":random_color}}
res3 = wm.send_template(user_id, template_id2, data2)
res4 = wm.send_template(my_user_id, template_id2, data2)