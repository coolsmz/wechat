# coding:utf-8
'''
@author: Sam_Shen
@file: cacti_func.py
@time: 2019/9/5 13:07
@desc: 
'''
import os
import datetime
import requests
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = datetime.datetime.now().strftime("%Y%m%d")
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
CACTI_FORM_DATA = {"login_username":"******************","login_password":"******************","action":"login"}
CACTI_LOGIN_URL = "http://172.20.9.28/index.php"
CACTI_LOGIN_COOKIE = None
CACTI_PNG_LIST = [{'command':'172.20.1.3#traffic','desc':'CU-SSG-172.20.1.3 - Traffic - ethernet2/0','local_graph_id':6868},
                  {'command': '172.20.1.3#cpu', 'desc': 'CU-SSG-172.20.1.3 - CPU Usage','local_graph_id': 3992},
                  ]

# 将时间字符串转换为10位时间戳
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


""" 获取cacti的登陆cookie """
def get_cacti_cookie():
    s = requests.session()
    # 首先用get方式登陆cacti获取cookie
    rs = s.post(CACTI_LOGIN_URL,headers=HEADER, data=CACTI_FORM_DATA)
    #利用RequestsCookieJar获取
    c = requests.cookies.RequestsCookieJar()
    c.set('cookie-name','cookie-value')
    s.cookies.update(c)
    global CACTI_LOGIN_COOKIE
    CACTI_LOGIN_COOKIE = s.cookies.get_dict()
    return CACTI_LOGIN_COOKIE

""" 获取cacti图片"""
def get_cacti_png(command):
    YESTERDAY = datetime.datetime.now() + datetime.timedelta(days=-1)
    YESTERDAY = YESTERDAY.strftime("%Y-%m-%d %H:%M:%S")
    TODAY = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for each in CACTI_PNG_LIST:
        if command == each['command']:
            local_graph_id = each['local_graph_id']
            png_url = "http://172.20.9.28/graph_image.php?local_graph_id=%s&rra_id=0&view_type=tree&graph_start=%s&graph_end=%s" % \
                      (local_graph_id, date_to_timestamp(YESTERDAY), date_to_timestamp(TODAY))

            response = requests.get(png_url, headers=HEADER, cookies=get_cacti_cookie())
            PNG_FILE = os.path.join(BASE_DIR,'common_static','img' ,str(local_graph_id) + '.png')
            with open(PNG_FILE,'wb') as f:
                f.write(response.content)
            return PNG_FILE