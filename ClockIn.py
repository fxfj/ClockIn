import requests
import json
from hashlib import md5
from urllib import parse
import time
import urllib3
import sys
urllib3.disable_warnings()


# --------------------------------------------------------------------------
phone = '13203879703'
pwd = 'lf553075327'
address = '河南省郑州市二七区长江路街道郑州航空工业管理学院'
lat = '113.646153'
lng = '34.716907'
district = '河南省-郑州市-二七区'
deviceToken = 'A517BB94-2D9C-49F4-B4A8-F0E32697BF09'
sckey = 'SCT86721TuMepNaHJZ1sSsOQ3bOCznQ03'
# ---------------------------------------------------------------------------
session = requests.Session()
date = time.strftime('%Y年%m月', time.localtime())
day = int(time.strftime('%d', time.localtime())) + 1  # 时间慢了一点，加一下
date = date + str(day)


# Wxpush()消息推送模块
def Wxpush(msg):
    url = f'https://sc.ftqq.com/{sckey}.send?text={date}日{msg}'
    for _ in range(3):
        err = requests.get(url)
        if not err.json()['errno']:
            break


# 指点天下登录模块
def login():
    url = 'http://app.zhidiantianxia.cn/api/Login/pwd'
    encoded_pwd = md5('axy_{}'.format(pwd).encode()).hexdigest()
    global flag
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '201',
        'Host': 'app.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.10.0'
    }
    data = {
        'phone': phone,
        'password': encoded_pwd,
        'mobileSystem': '10',
        'appVersion': '1.6.4',
        'mobileVersion': 'Mate30',
        'deviceToken': deviceToken,
        'pushToken': '0938765546475757478765800CN01',
        'romInfo': 'hw'
    }

    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print('login_success!')
        flag = 1
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Wxpush(msg)
        flag = 0
    return response.json()['data']


# 每日健康打卡模块
def sign_in(token):
    url = 'http://zua.zhidiantianxia.cn/api/study/health/apply'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'TAS-AN00(Android/5.1.1) (com.axy.zhidian/1.5.5) Weex/0.18.0 720x1280',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '536'
    }
    content = {"location": {"address": address, "lat": lat, "lng": lng, "code": "1"}, "temperature": "36.6",
                        "health": "是", "observation": "否", "confirmed": "否", "haveCOVIDInPlaceOfAbode": "否",
                        "goToHuiBei": "否", "contactIllPerson": "否", "haveYouEverBeenAbroad": "否",
                        "familyPeopleNum": "4", "isFamilyHealth": "否", "isFamilyColdChain": "否", "isFamilyStatus": "否",
                        "familyPeopleIsAway": "否", "hasYourFamilyEverBeenAbroad": "否", "leave": "否",
                        "isYesterdayMove": "否", "admission": "是", "help": "", "nowLocation": district}
    data = {"health": 0,
            "student": 1,
            "templateId": 2,
            "content": str(content)}
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        msg = '打卡成功'
        Wxpush(msg)
    else:
        msg = parse.quote_plus(response.json()['msg'])
        Wxpush(msg)


# 获取每日宿舍签到的signInId模块
def get_signInId(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/my'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'user-agent': 'TAS-AN00(Android/5.1.1) (com.axy.zhidian/1.5.5) Weex/0.18.0 720x1280',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    data = {
        'page': '0',
        'size': '10'
    }
    try:
        signInId = session.get(url=url, headers=header, data=data).json()['data']['content'][0]['id']
        return signInId
    except:
        pass


# 22点宿舍签到模块
def sign_in_evening(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/sign'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'TAS-AN00(Android/5.1.1) (com.axy.zhidian/1.5.5) Weex/0.18.0 720x1280',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '146'
    }
    data = {
        "locale": address,
        "lat": lat,
        "lng": lng,
        "signInId": get_signInId(token)
    }
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print("success!")
    else:
        print("fail!")
    msg = parse.quote_plus(response.json()['msg'])
    Wxpush(msg)


if __name__ == "__main__":
    token = login()
    time.sleep(3)
    now_H = int(time.strftime("%H"))
    sign_in(token)
