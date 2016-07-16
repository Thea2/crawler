# coding=utf-8

import urllib2
import re
import Momi
import threading
import semantic

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}
a = Momi.MoblieWeibo()
a.login('oktong668an@163.com', 'pachong13')


class GetNews:    # 获取某媒体热点新闻的类

    def __init__(self, baseURL, uid, file_name, page_num):
        """
        初始化
        :param baseURL:基本链接
        :param uid: 该媒体的用户id
        :param file_name: 存储热点新闻的文件名
        :param page_num: 获取媒体前几页的热点新闻
        """
        self.baseURL = baseURL
        self.uid = uid
        self.file_name = file_name
        self.page_num = page_num

    def get_page(self, page_num):
        """
        获取某网页的源代码
        :param page_num:网页在为该博主的第几个页面
        :return: 网页的源代码
        """
        try:
            url = self.baseURL+str(self.uid)+'?page='+str(page_num)
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    def get_new_content(self, page):
        """
        获取热点新闻
        :param page: 网页源代码
        :return: 热点新闻列表
        """
        news = []
        content_pattern = re.compile('<div class="c".*?<span class="ctt">(.*?)</span>'
                                     '.*?赞\[(\d*)].*?转发\[(\d*)].*?评论\[(\d*)]')
        more_link_pattern = re.compile('<a href=\'/(.*?)\'>全文<')
        more_content_pattern = re.compile('<div class="c" id="M_">.*?<span class="ctt">(.*?)</span>')
        pattern = re.compile('<.*?>')
        content = re.findall(content_pattern, page)
        for x in content:
            if (x[1] > 50) and (x[2] > 100) and (x[3] > 50):    # x[0]为微博正文，x[1]为该博文赞的数量，x[2]为该博文转发的数量，x[3]为该博文评论的数量
                if '>全文<' in x[0]:    # 若在当前网页不能显示微博全文则进一步获取正文全文
                    more_link = re.findall(more_link_pattern, x[0])
                    for link in more_link:
                        more_url = self.baseURL+link
                    more_req = urllib2.Request(more_url, headers=headers)
                    more_response = urllib2.urlopen(more_req)
                    more_page = more_response.read()
                    more_content = re.findall(more_content_pattern, more_page)
                    for main_content in more_content:
                        new = main_content
                        new = re.sub(pattern, '', new)
                else:
                    new = re.sub(pattern, '', x[0])
                news.append(new)
                print new
        return news

    def save_data(self, new):    # 将热点新闻存入指定文件
        f = open(self.file_name, 'a')
        f.write(new + '\n')
        f.close()

    def start(self):    # 开始工作～
        for i in range(int(self.page_num)):
            page = self.get_page(i + 1)
            news = self.get_new_content(page)
            for new in news:
                self.save_data(new)


if __name__ == '__main__':
    base_url = 'http://weibo.cn/'
    media = {'jinritoutiao': {'user_id': '2745813247', 'file_name': 'dataSet/jinritoutiao'},
             'sohu': {'user_id': '2083844833', 'file_name': 'dataSet/sohu'},
             'wangyi': {'user_id': '1974808274', 'file_name': 'dataSet/wangyi'},
             'fenghuang': {'user_id': '1992613670', 'file_name': 'dataSet/fenghuang'},
             'yangshi': {'user_id': '2656274875', 'file_name': 'dataSet/yangshi'}}
    threads = []
    for m in media:
        get_news = GetNews(base_url, media[m]['user_id'], media[m]['file_name'], 2)
        t1 = threading.Thread(target=get_news.start())
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
