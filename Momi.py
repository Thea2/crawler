# coding:utf-8
__author__ = 'chenge'
import re
import urllib2
import urllib
import cookielib

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class MoblieWeibo:  # 模拟登陆
    def __init__(self):
        # self.cap = None
        self.cj = cookielib.LWPCookieJar()
        # if cookie_j.load(cookie_filename)
        # 将一个保存cofilename is not None:
        #     self.cj.load(cookie_filename)
        # 将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        # 创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
        self.opener = urllib2.build_opener(self.cookie_processor,
                                           urllib2.HTTPHandler)  # 将包含了cookie、http处理器、http的handler的资源和urllib2对象绑定在一起
        urllib2.install_opener(self.opener)

    def getArgs(self):
        ArgsRequest = urllib2.Request('http://login.weibo.cn/login/', headers=headers)
        response = urllib2.urlopen(ArgsRequest)
        text = response.read()

        # print "获取post数据中的vk的值:"
        vkPattern = re.compile('<input type="hidden" name="vk" value="(.*?)" />')
        self.vk = re.search(vkPattern, text).group(1)
        # print self.vk

        # print "获取post数据中的backURL的值:"
        self.BackUrlPattern = re.compile("<input type=\"hidden\" name=\"backURL\" value=\"(.*?)\" />")
        self.BackUrl = re.search(self.BackUrlPattern, text).group(1)
        # print self.BackUrl

        # print "获取post数据中的rand的值:"
        randPattern = re.compile('<form action="\?rand=(.*?)&')
        self.rand = re.search(randPattern, text).group(1)
        # print self.rand

        # print "获取post数据中的passwd变量的值:"
        pwdPattern = re.compile('<input type="password" name="(.*?)" size="30" />')
        self.passwd = re.search(pwdPattern, text).group(1)
        # print self.passwd

        capPattern = re.compile('<input type="hidden" name="capId" value=\"(.*?)\" />')
        self.cap = re.search(capPattern, text).group(1)
        # print self.cap

        Img = re.compile('<img src="(.*?)" alt="请打开图片显示" />')
        img = re.search(Img, text).group(1)
        print img
        code = raw_input('请输入验证码')
        self.text = code

    def login(self, username, password):
        # print username,password
        self.getArgs()
        # print "生成post数据,向网址Url提交post:"
        PostData = {
            "mobile": username,
            str(self.passwd): password,
            'code': self.text,
            'submit': "登录",
            'remember': "checked",
            'backURL': self.BackUrl,
            'vk': self.vk,
            'tryCount': '',
            'capId': self.cap,
            'rand': self.rand
        }
        # print PostData
        PostData = urllib.urlencode(PostData)
        # print "输出调交post返回的主页:"
        request = urllib2.Request('http://login.weibo.cn/login/', PostData, headers)
        response = urllib2.urlopen(request)
        text = response.read()
        while '我的首页' not in text:  # 检验验证码是否正确
            print '验证码错误，请重输'
            m = MoblieWeibo()
            m.login(username, password)
            break
