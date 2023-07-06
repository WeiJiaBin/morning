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
# template_id = os.environ["TEMPLATE_ID"]
template_id = "Fi1tmeT3E0Bcff3mKp7LVXZ3wsoBwpVYs0MMrUVPU7Q"
he_feng_key = os.environ["APP_KEY"]
locationMap={
    '101300601':"梧州",
    '101190107':"南京",
}

def get_weather():
    hefeng_key = he_feng_key
    location = '101300601'  #'101190107'
    url = "https://devapi.qweather.com/v7/weather/now?key=" + hefeng_key + "&location=" + location
    res = requests.get(url).json()
    weather = res['now']
    weather['text'] = locationMap[location] + "-" + weather['text']
    return weather['text'], weather['feelsLike']


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# def get_words():
#     words = requests.get("https://api.shadiao.pro/chp")
#     if words.status_code != 200:
#         return get_words()
#     return words.json()['data']['text']
def get_words():
  # words = requests.get("https://api.shadiao.pro/chp")
  # if words.status_code != 200:
  #   return get_words()
  # return words.json()['data']['text']
  words = requests.get("https://apis.tianapi.com/saylove/index?key=6456a75fa758f057ff512acc785037a8")

  if words.status_code != 200:
    return get_words()
  return words.json()['result']['content']

def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def split_string(string):
    return [string[i:i + 20] for i in range(0, len(string), 20)]


get_words_text = ''
get_words_text1 = ''
get_words_text2 = ''
get_words_text3 = ''
get_words_text4 = ''
get_words_text5 = ''

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
get_words_text = get_words()
textlist = split_string(get_words_text)
for index in range(len(textlist)):
    text_con = textlist[index]
    if index == 0:
        get_words_text1 = text_con
    if index == 1:
        get_words_text2 = text_con
    if index == 2:
        get_words_text3 = text_con
    if index == 3:
        get_words_text4 = text_con
    if index == 4:
        get_words_text5 = text_con
random_color = get_random_color()
# wea, temperature = "小宝宝", "520"
data = {"weather": {"value": wea}, "temperature": {"value": temperature}, "love_days": {"value": get_count()},
        "birthday_left": {"value": get_birthday()}
    , "words": {"value": get_words_text1, "color": random_color}
    , "words2": {"value": get_words_text2, "color": random_color}
    , "words3": {"value": get_words_text3, "color": random_color}
    , "words4": {"value": get_words_text4, "color": random_color}
    , "words5": {"value": get_words_text5, "color": random_color}
        }
res = wm.send_template(user_id, template_id, data)
res2 = wm.send_template(my_user_id, template_id, data)
print(res)
# print(res2)
# template_id2 = "BW6sZBjGCVxZ4n648OPYD6nqYDEViMHAMCQTBhX-6y0"
# data2 = {"words":{"value":get_words_text, "color":random_color}}
# res3 = wm.send_template(user_id, template_id2, data2)
# res4 = wm.send_template(my_user_id, template_id2, data2)
