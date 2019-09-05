# coding:utf-8
'''
@author: Sam_Shen
@file: func.py
@time: 2019/9/5 12:58
@desc: 
'''

from robot import get_access_token_class
import re
import requests


# 获取上传文件的media_ID,发图片的时候，必须使用该api提供的media_ID
def get_media_ID(file):
    img_url='https://api.weixin.qq.com/cgi-bin/media/upload'
    payload_img={
        'access_token':get_access_token_class.GET_ACCESS_TOKEN(),
        'type':'image'
    }

    data = {'media':open(file,'rb')}
    r = requests.post(url=img_url,params=payload_img,files=data)
    dict = r.json()
    print(dict)
    return dict['media_id']


QUERY_CONTENT = ['cpu','menory','disk','tcp','process','traffic_in','traffic_out']
def check_command_for_equipment(STR):
    try:
        str_list = STR.split('#')
        ip_address = str_list[0]
        ip_content = str_list[1]

        if not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",ip_address):
            return False

        elif ip_content not in QUERY_CONTENT:
            return False

        else:
            return STR

    except:
        return False