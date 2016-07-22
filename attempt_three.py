# coding: utf-8

import sys
import re
import Momi
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class Info(object):    # 根据用户名得到用户基本资料的类

    def __init__(self, username):    # 初始化
        self.username = username

    def get_page(self, url):
        """
        获取某网页的源代码
        :param url: 某网页的链接
        :return: 某网页的源代码
        """
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.URLError as e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    def get_someone_table(self, search_page):
        """
        获取搜索结果页面显示的第一个用户信息表格
        :param search_page: 搜索结果页面源代码
        :return: 用户信息表格
        """
        pattern = re.compile('<table>(.*?)</table>')
        someone_table = re.search(pattern, search_page).group()
        return someone_table

    def get_uid_no_attention(self, someone_table):
        """
        获取未关注的用户id
        :param someone_table:用户信息表格
        :return: 用户id
        """
        uid_pattern = re.compile('uid=(.*?)&amp')
        uid = re.search(uid_pattern, someone_table).group(1)
        return uid

    def get_uid_attention(self, someone_table):
        """
        获取已关注的用户id
        :param someone_table:用户信息表格
        :return: 用户id
        """
        index_pattern = re.compile('<td valign="top"><a href="(.*?)">')
        index_part = re.search(index_pattern, someone_table).group(1)
        index_url = 'http://weibo.cn%s' % index_part    # 用户首页链接
        index_page = self.get_page(index_url)
        uid_pattern = re.compile('&nbsp;<a href="/(.*?)/info">资料')
        uid = re.search(uid_pattern, index_page).group(1)
        return uid

    def get_user_info(self, uid):
        """
        获取用户基本信息
        :param uid: 用户id
        :return: 用户基本信息
        """
        user_info_url = 'http://weibo.cn/%s/info' % uid
        user_info_page = self.get_page(user_info_url)
        sex_pattern = re.compile('性别:(.*?)<br/>')
        area_pattern = re.compile('地区:(.*?)<br/>')
        birth_pattern = re.compile('生日:(\d*?)-.*?<br/>')
        sex = re.search(sex_pattern, user_info_page)
        area = re.search(area_pattern, user_info_page)
        birth = re.search(birth_pattern, user_info_page)
        if sex:
            sex = sex.group(1)
        if area:
            area = area.group(1)
        if birth:
            birth = birth.group(1)
            if int(birth) != 0001:    # 将年龄为微博默认设置的用户过滤
                info = {'性别': sex, '地区': area, '年龄': 2016-int(birth)}
                return info
        info = {'性别': sex, '地区': area, '年龄': None}
        return info

    def show_user_info(self, user_info):
        """
        展示用户基本信息
        :param user_info:用户基本信息
        """
        for key in user_info:
            if user_info[key]:
                print key, user_info[key]
            else:
                print key, '未知'

    def main(self):
        search_url = 'http://weibo.cn/find/user?keyword=%s&suser=1' % self.username    # 搜索结果页面链接
        search_page = self.get_page(search_url)
        someone_table = self.get_someone_table(search_page)
        if '已关注' in someone_table:
            user_id = self.get_uid_attention(someone_table)
        else:
            user_id = self.get_uid_no_attention(someone_table)
        user_info = self.get_user_info(user_id)
        self.show_user_info(user_info)


if __name__ == '__main__':
    a = Momi.MoblieWeibo()
    a.login('oktong668an@163.com', 'pachong13')
    while 1:
        username = raw_input('请输入用户昵称：')
        user = Info(username)
        user.main()
        flag = raw_input('继续搜索请输入1，停止搜索请输入0:')
        if int(flag) == 0:
            print 'end'
            break
