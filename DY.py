#!/usr/bin/env python
# encoding: utf-8
import re
import requests
import os
from bs4 import BeautifulSoup
from common import *

# 获取Token       有效期60分钟
token = getToken()
# 获取新的设备信息  有效期永久
device_info = getDevice()





def download(aweme_id,userid):

    if not os.path.exists(os.getcwd() + f"\{userid}"):
        os.makedirs(os.getcwd() + f"\{userid}")
        print('新用户！！！')
    else:
        print('注意！！！同一个用户！！！')
    for i in aweme_id:
        params = {
            "iid": device_info['iid'],
            "idfa": device_info['idfa'],
            "vid": device_info['vid'],
            "device_id": device_info['device_id'],
            "openudid": device_info['openudid'],
            "device_type": device_info['device_type'],
            "os_version": device_info['os_version'],
            "os_api": device_info['os_api'],
            "screen_width": device_info['screen_width'],
            "device_platform": device_info['device_platform'],
            "version_code": APPINFO['version_code'],
            "channel": APPINFO['channel'],
            "app_name": APPINFO['app_name'],
            "build_number": APPINFO['build_number'],
            "app_version": APPINFO['app_version'],
            "aid": APPINFO['aid'],
            "ac": "WIFI",
        }

        postParams = {
            "aweme_id": i
        }

        signParams = params
        signParams.update(postParams)
        sign = getSign(token, signParams)
        params['mas'] = sign['mas']
        params['as'] = sign['as']
        params['ts'] = sign['ts']
        print(params)
        # 获取视频详情
        resp = requests.get("https://aweme.snssdk.com/aweme/v1/aweme/detail/", params=params, data=postParams,
                            headers=header).json()
        print(resp)
        play_addr = resp['aweme_detail']['video']['play_addr']['url_list'][0]
        print(u"下载地址: " + play_addr)
        saveFile = os.getcwd()+rf"\{str(userid)}" + f"\{i }.mp4"
        resp = requests.get(play_addr)
        open(saveFile, "wb").write(resp.content)


#获取用户长地址
def get_userid(url):
    reps = requests.get(url,headers=header)
    print(reps)
    useid = reps.url.split('?')[0].split('/')[5]  #获取用户id
    soup = BeautifulSoup(reps.text,'html.parser')
    dytk = soup.find_all('script',type='text/javascript')
    dytk = re.findall("dytk: '(.*)'",str(dytk))[0]
    return useid,dytk

#执行js代码获取_Signature
def generateSignature(userid):
    p = os.popen('node fuck-byted-acrawler.js %s' % str(userid))
    return p.readlines()[0]
def get_user_data(surl,header):
    all=get_userid(surl)
    userid = all[0]
    dytk = all[1]
    Signature = generateSignature(userid)
    print(Signature)
    print(dytk)
    newsurl = f'https://www.iesdouyin.com/aweme/v1/aweme/post/?user_id={str(userid.rstrip())}&count=21&max_cursor=0&aid=1128&_signature={Signature.strip()}&dytk={dytk.strip()}'
    print(newsurl)
    data = requests.get(newsurl, headers=header, allow_redirects=False).json()
    while len(data) <= 3:
        aweme_id = []
        data = requests.get(newsurl, headers=header, allow_redirects=False).json()
        print(data['aweme_list'])
        for i in data['aweme_list']:
            print(i['aweme_id'])
            aweme_id.append(i['aweme_id'])
    else:
        data = requests.get(newsurl, headers=header, allow_redirects=False).json()
    return aweme_id,userid
if __name__ == '__main__':
    import time
    header = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) "
                      "Version/11.0 Mobile/15A372 Safari/604.1",
    }
    print('*'*60)
    print(' '*15,'抖音高清无水印下载')
    print('*'*60)
    with open(os.getcwd()+r"\地址.txt")as f:
    	surl=f.readline()
    all_id = get_user_data(surl,header)
    userid = all_id[1]
    awemeid = all_id[0]
    download(awemeid,userid)
    print('*'*60)
    print(' '*20,'下载完成,感谢您的使用')
    print('*' * 60)
