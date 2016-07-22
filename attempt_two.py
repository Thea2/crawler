# coding=utf-8
import urllib2
import urllib
import cookielib
import re


def login():    # 登陆学生个人中心查询成绩
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
    }
    cj = cookielib.LWPCookieJar()
    cookie_processor = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_processor, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    while 1:
        data = {
            'USERNAME': raw_input('username:'),
            'PASSWORD': raw_input('password:')
        }
        postdata = urllib.urlencode(data)
        request = urllib2.Request('http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap', postdata, headers)
        response = urllib2.urlopen(request)
        text = response.read()
        if '我的桌面' in text:
            print '登陆成功'
            break
    while 1:
        request = urllib2.Request('http://jxgl.gdufs.edu.cn/jsxsd/kscj/cjcx_list')
        response = urllib2.urlopen(request)
        text = response.read()
        if '查询列表' in text:
            print '进入查询列表'
            break
    content_pattern = re.compile('<tr>([\w\W]*?)</tr>')
    content = re.findall(content_pattern, text)
    content_list = []
    for each in content:
        line_list = []
        each = re.sub('<[\w\W]*?>', '', each)
        each = each.split()
        for every in each:
            line_list.append(every)
        content_list.append(line_list)
    for score in content_list:
        if score:
            print score[3], score[4]


if __name__ == '__main__':
    login()