#!/usr/bin/env python
# -*- encoding=utf8 -*-

import json
import random
import requests
import os
import time
import smtplib
import logging
import datetime


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from .config import global_config
from .jd_logger import logger

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
]


def parse_json(s):
    begin = s.find('{')
    end = s.rfind('}') + 1
    return json.loads(s[begin:end])


def get_random_useragent():
    """生成随机的UserAgent
    :return: UserAgent字符串
    """
    return random.choice(USER_AGENTS)


def wait_some_time():
    time.sleep(random.randint(100, 300) / 1000)


def send_wechat(message):
    """推送信息到微信"""
    url = 'http://sc.ftqq.com/{}.send'.format(global_config.getRaw('messenger', 'server_chan_sckey'))
    payload = {
        "text": '抢购结果',
        "desp": message
    }
    headers = {
        'User-Agent': global_config.getRaw('config', 'default_user_agent')
    }
    requests.get(url, params=payload, headers=headers)


def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


def open_image(image_file):
    if os.name == "nt":
        os.system('start ' + image_file)  # for Windows
    else:
        if os.uname()[0] == "Linux":
            if "deepin" in os.uname()[2]:
                os.system("deepin-image-viewer " + image_file)  # for deepin
            else:
                os.system("eog " + image_file)  # for Linux
        else:
            os.system("open " + image_file)  # for Mac


def save_image(resp, image_file):
    with open(image_file, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            f.write(chunk)


def add_bg_for_qr(qr_path):
    try:
        from PIL import Image
        qr = Image.open(qr_path)
        w = qr.width
        h = qr.width
        bg = Image.new("RGBA", (w * 2, h * 2), (255, 255, 255))
        result = Image.new(bg.mode, (w * 2, h * 2))
        result.paste(bg, box=(0, 0))
        result.paste(qr, box=(int(w / 2), int(h / 2)))
        result.save(qr_path)
        return os.path.abspath(qr_path)
    except ImportError:
        logger.info("加载PIL失败，不对登录二维码进行优化，请查看requirements.txt")
        return qr_path


class Email():

    def __init__(self, mail_user, mail_pwd, mail_host=''):
        if global_config.getRaw('messenger', 'email_enable') == 'false':
            return

        smtpObj = smtplib.SMTP()
        # 没传会自动判断 判断不出来默认QQ邮箱
        if mail_host:
            self.mail_host = mail_host
        elif mail_user.endswith('163.com'):
            self.mail_host = 'smtp.163.com'
        elif mail_user.endswith(('sina.com', 'sina.cn')):
            self.mail_host = 'smtp.163.com'
        elif mail_user.endswith('qq.com'):
            self.mail_host = 'smtp.qq.com'
        elif mail_user.endswith('sohu.com'):
            self.mail_host = 'smtp.sohu.com'
        else:
            self.mail_host = 'smtp.qq.com'
        self.mail_user = mail_user
        self.is_login = False
        try:
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pwd)
            self.is_login = True
        except Exception as e:
            logger.info('邮箱登录失败!', e)
        self.smtpObj = smtpObj

    def send(self, title, msg, receivers: list, img=''):
        """
        发送smtp邮件至收件人
        :param title:
        :param msg: 如果发送图片，需在msg内嵌入<img src='cid:xxx'>，xxx为图片名
        :param receivers:
        :param img: 图片名
        :return:
        """
        if self.is_login:
            message = MIMEMultipart('alternative')
            msg_html = MIMEText(msg, 'html', 'utf-8')
            message.attach(msg_html)
            message['Subject'] = title
            message['From'] = self.mail_user
            if img:
                with open(img, "rb") as f:
                    msg_img = MIMEImage(f.read())
                msg_img.add_header('Content-ID', img)
                message.attach(msg_img)
            try:
                self.smtpObj.sendmail(self.mail_user, receivers, message.as_string())
            except Exception as e:
                logger.info('邮件发送失败!', e)
        else:
            logger.info('邮箱未登录')


"""
message_content
{"title":"Homeassistant","message":"text|内容"}
{"title":"Homeassistant","message":"news|内容|打开链接|图片链接"}
{"title":"Homeassistant","message":"textcard|内容|打开链接"}
{"title":"Homeassistant","message":"video|内容|mp4本地地址"}
"""
class Qiyeweichat():

    def __init__(self, corpid, agentId, secret, touser):
        if global_config.getRaw('messenger', 'qywx_enable') == 'false':
            return
        self.CORPID = corpid
        self.CORPSECRET = secret
        self.AGENTID = agentId
        self.TOUSER = touser

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        access_token = self._get_access_token()
        return access_token

    def send_message(self, message_content):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        title = message_content["title"]
        message = message_content["message"]
        if title:
           timestp = datetime.datetime.now()
           sendtime = '{} {}'.format(timestp.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日'), timestp.strftime("%H:%M:%S"))

           msgtype = message.split('|')[0]
           if msgtype == 'text' :
             message = '"content":' + '"' + title + '\r\n' + '--------------------------------------------' + '\r\n' + message.split('|')[1] + '\r\n' + '--------------------------------------------' + '\r\n' + sendtime + '"'
           elif  msgtype == 'textcard' :
             message = '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"' + ',' + '"url":' + '"' + message.split('|')[2] + '"'
           elif  msgtype == 'news' :
             message ='"articles":[{' + '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"' + ',' + '"url":' + '"' + message.split('|')[2] + '"' + ',' + '"picurl":' + '"' + message.split('|')[3] + '"' + '}]'
           elif  msgtype == 'video' :
               path = message.split('|')[2]
               curl = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.get_access_token() + '&type=video'
               files = {'video': open(path, 'rb')}
               r = requests.post(curl, files=files)
               re = json.loads(r.text)
               ree = re['media_id']
               media_id = str(ree)
               message = '"media_id":' + '"' + media_id + '"' + ',' + '"title":' + '"' + title + '"' + ',' + '"description":' + '"' + message.split('|')[1] + '\r\n' + sendtime + '"'
           else:
             msgtype = 'text'
             message = '"content":' + '"' + message.split('|')[1] + '"'
           send_data = '{"msgtype": "%s", "safe": "0", "agentid": %s, "touser": "%s", "%s": {%s}}' % (
               msgtype, self.AGENTID, self.TOUSER, msgtype, message)
           send_data8 = send_data.encode('utf-8')
           response = requests.post(send_url,send_data8)
        else:
           _LOGGER.error("Title can NOT be null")


email = Email(
    mail_host=global_config.getRaw('messenger', 'email_host'),
    mail_user=global_config.getRaw('messenger', 'email_user'),
    mail_pwd=global_config.getRaw('messenger', 'email_pwd')
)

qywx = Qiyeweichat(
    qywx_corpid=global_config.getRaw('messenger', 'qywx_corpid'),
    qywx_agentId=global_config.getRaw('messenger', 'qywx_agentId'),
    qywx_secret=global_config.getRaw('messenger', 'qywx_secret'),
    qywx_touser=global_config.getRaw('messenger', 'qywx_touser')
)
