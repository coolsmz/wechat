from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from xml.etree import ElementTree as ET
import time
from django.utils.encoding import smart_str
from robot import func
from robot import cacti_func


WECHAT_TOKEN = '******************'

class Analysis:
    def __init__(self, xmlData):
        print("接收到的数据：" + xmlData)

    def prase(self, xmlText):
        xmlData = ET.fromstring(xmlText)
        msgType = xmlData.find("MsgType").text
        toUserName = xmlData.find("ToUserName").text
        fromUserName= xmlData.find("FromUserName").text
        if msgType == 'text':
            content = xmlData.find("Content").text

        if content == '你好':
            content = '''
            你好,我是寰亚小机器人,我只有一些简单的小功能.
            当然只要你输入对了指令,我会芝麻开门给你惊喜.
            更多更高级的功能,我的主人还在开发中.
            '''
            TextMsgObj = TextMsg(toUserName, fromUserName, content)
            return TextMsgObj.structReply()

        if content == '芝麻开门':
            content = '哈哈哈,芝麻开门可不是指令哦.'
            TextMsgObj = TextMsg(toUserName, fromUserName, content)
            return TextMsgObj.structReply()

        if func.check_command_for_equipment(content):
            command = func.check_command_for_equipment(content)
            cacti_png = cacti_func.get_cacti_png(command)
            mediaId = func.get_media_ID(cacti_png)
            ImageMsgObj = ImageMsg(toUserName,fromUserName,mediaId)
            return ImageMsgObj.structReply()

        if content == 'movie':
            mediaId = func.get_media_ID('common_static/img/p2555886490.jpg')
            ImageMsgObj = ImageMsg(toUserName,fromUserName,mediaId)
            return ImageMsgObj.structReply()

        else:
            content = '我还在开发中'
            TextMsgObj = TextMsg(toUserName, fromUserName, content)
            return TextMsgObj.structReply()

class ImageMsg:
    def __init__(self,toUser,fromUser,mediaId):
        self._toUser = toUser
        self._fromUser = fromUser
        self._rediaId = mediaId
        self._nowTime = int(time.time())
        self._mediaId = mediaId

    def structReply(self):
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{3}]]></MediaId>
                </Image>
                </xml>
                """.format(self._fromUser, self._toUser,self._nowTime,self._mediaId)   #前面两个参数的顺序需要特别注意
        return text

class TextMsg:
    def __init__(self,toUser,fromUser,recvMsg):
        self._toUser = toUser
        self._fromUser = fromUser
        self._recvMsg = recvMsg
        self._nowTime = int(time.time())

    def structReply(self):
        content = self._recvMsg
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{3}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser,self._nowTime,content)   #前面两个参数的顺序需要特别注意

        return text


@csrf_exempt
def wechat(request):
    if request.method == 'GET':
        print('GET请求来了--------')
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response

    elif request.method == 'POST':
        print("POST请求来了--------")

        msg = parse_message(request.body)
        if msg.type == 'text':
            analysisObj = Analysis(smart_str(request.body))
            print('smart_str',smart_str(request.body))

            toWxData = analysisObj.prase(smart_str(request.body))
            print(toWxData)
            return HttpResponse(smart_str(toWxData))


        elif msg.type == 'image':
            reply = create_reply('这是条图片消息,图片信息我可看不懂/:P-(/:P-(/:P-(', msg)
            response = HttpResponse(reply.render(), content_type="application/xml")
            return response

        elif msg.type == 'voice':
            reply = create_reply('这是条语音消息,语音信息我也听不懂/:P-(/:P-(/:P-(', msg)
            response = HttpResponse(reply.render(), content_type="application/xml")
            return response

        else:
            reply = create_reply('这是条其他类型消息,暂时不处理', msg)
            response = HttpResponse(reply.render(), content_type="application/xml")
            return response

    else:
        print('--------------------------------')
