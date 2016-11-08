#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.4"
Update
- name   : "wangmengcn"
- email  : "eclipse_sv@163.com"
- date   : "2016.4.21"
'''
import requests
import openpyxl
from bs4 import BeautifulSoup


try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path

try:
    from PIL import Image
except:
    pass

# 构造 Request headers
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
headers = {
    "Host": "www.shanxinhui.com",
    "Referer": "https://www.shanxinhui.com/",
    "User-Agent": agent,
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    print('get cookies')
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.shanxinhui.com/User/Public/verify/' + t
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "http://www.shanxinhui.com/User/Manager/ListUserOutGo"
    login_page = session.get(url, headers=headers, allow_redirects=False)
    print(login_page.text)
    print('-------------------------------2222')
    wb = openpyxl.load_workbook(filename='sxh.xlsx')
    ws=wb.create_sheet(title='go1go')

    html = open('index.html', encoding="utf-8").read()
    okok = html.replace('</td>\n</td>','</td>')
    print('-------------------------------A')

    # print(okok)
    soup = BeautifulSoup(okok, "html.parser")
    # soup = BeautifulSoup(login_page.text, "html.parser")
    # print(soup.find("table"))
    rows = soup.find("table").find_all("tr")
    print('-------------------------------A')
    print(rows)
    dict =  {'123456': [1,2]}
    array = [dict]

    # print(rows[0])
    rows.pop()
    for idx, row in enumerate(rows):
        cells = row.find_all("td")
        print(cells[3])
        for idxx, val in enumerate(cells):

            # if val.get_text() == '善种子':
            #     print("这是一个山种子")
            # print(val.get_text())
            ws.cell(row=idx + 1, column=idxx + 1).value = val.get_text()

    wb.save(filename='sxh.xlsx')




        # print(rn)

    print('---')
    # if login_page.status_code == 200:
    #     return True
    # else:
    #     return False


def login(secret, account):
    # 通过输入的用户名判断是否是手机号
    print("手机号登录 \n")
    post_url = 'http://www.shanxinhui.com/User/Public/login'
    postdata = {
        'password': secret,
        'username': account,
        'verify': 3169,
    }

    # 需要输入验证码后才能登录成功
    postdata["verify"] = get_captcha()
    login_page = session.post(post_url, data=postdata, headers=headers)
    print(login_page.text)
    # login_code = eval(login_page.text)
    # print(login_code)
    print(type(session.cookies))
    print(session.cookies)
    # session.cookies.save()


def writeExcel():
    wb = openpyxl.load_workbook(filename='sxh.xlsx')
    ws=wb.create_sheet(title='hahah')
    ws.cell(row=1, column=1).value = 1232132
    wb.save(filename='sxh.xlsx')

try:
    input = raw_input
except:
    pass

if __name__ == '__main__':
    print('哈哈')
    # writeExcel()
    # login('ss9988', 'csy9988')
    if isLogin():
        print('您已经登录')
    # else:
    #     account = input('请输入你的用户名\n>  ')
    #     secret = input("请输入你的密码\n>  ")
    #     login(secret, account)
