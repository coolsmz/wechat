# coding:utf-8
'''
@author: Sam_Shen
@file: get_access_token_class.py
@time: 2019/9/3 14:47
@desc: 
在微信公众号开发中,使用api都要附加access_token内容,因此首先需要获取access_token
access_token每2小时过期
所以尝试用pickle存储access_token
每次调用access_token前,先pickle load pkl文件进行时间比较
如果没有拆过2小时,就直接调用存储的access_token
如果已经超过2小时,就获取新的access_token
'''

import pickle
import datetime
import requests
import os

class GET_ACCESS_TOKEN:
    def __init__(self):
        self.HOURS_2 = 60*60*2
        self.WORK_DIR = os.path.dirname(os.path.abspath(__file__))
        self.PKL_FILE = os.path.join(self.WORK_DIR,'ACCESS_TOKEN.pkl')
        self.GRANT_TYPE = "client_credential",
        self.APPID = "******************"
        self.SECRET = "******************",

    def from_wechat_get_access_token(self):
        # 获取微信全局接口的凭证(默认有效期俩个小时)
        result = requests.get(
            url = "https://api.weixin.qq.com/cgi-bin/token",
            params = {
                "grant_type": self.GRANT_TYPE,
                "appid": self.APPID,
                "secret": self.SECRET,
            }
        ).json()
        if result.get("access_token"):
            access_token = result.get('access_token')
        else:
            access_token = None
        return access_token

    # 将access_token获取信息写入pkl文件
    def write_ac_to_pkl(self):
        get_time = datetime.datetime.now()
        access_token = {"get_time":get_time,"access_token":self.from_wechat_get_access_token()}
        pickle_file = open(self.PKL_FILE,'wb')
        pickle.dump(access_token,pickle_file)
        pickle_file.close()

    # 读取pkl并进行时间比较,没有超过2小时,return access_token,超过2小时,return False
    def read_from_pkl(self):
        read_time = datetime.datetime.now()
        pickle_file = open(self.PKL_FILE, 'rb')
        access_token = pickle.load(pickle_file)

        get_time = access_token['get_time']
        seconds_differ = (read_time-get_time).seconds

        if seconds_differ < self.HOURS_2:
            return access_token['access_token']
        else:
            return False

    def __str__(self):
        if os.path.exists(self.PKL_FILE):
            if not self.read_from_pkl():
                self.write_ac_to_pkl()
        else:
            self.write_ac_to_pkl()

        access_token = self.read_from_pkl()
        return access_token