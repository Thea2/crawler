# coding=utf-8

import Momi
import urllib2
import re
import multiprocessing
import threading

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


def select_info(i):    # 选择特定的微博正文并输出
    url = "http://weibo.cn/headlineapp?page=%d" % (i+1)
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    text = response.read()
    content_pattern = re.compile('<div class="c".*?<span class="ctt">([\w\W].*?)</span>'    # 匹配微博正文
                                 '.*?<a href="http://weibo\.cn/attitude/.*?>.*?(\d*)]</a>'    # 匹配该微博的赞的数量
                                 '.*?<a href="http://weibo\.cn/repost/.*?>.*?(\d*)]</a>'    # 匹配该微博转发的数量
                                 '.*?<a href="http://weibo\.cn/comment/.*?>.*?(\d*)]</a>')    # 匹配该微博评论的数量
    pattern = re.compile('<.*?>')
    content = re.findall(content_pattern, text)
    for x in content:
        if x[1] > 20:   # 判断微博的赞的数量是否大于20（输出微博正文的满足条件）
            x = re.sub(pattern, '', str(x[0]))    # 去掉微博正文中的链接等不需要的东西
            print x


if __name__ == '__main__':
    a = Momi.MoblieWeibo()
    a.login(13423625046, 'zhou970713')
    for i in range(5):    # 多进程
        p = multiprocessing.Process(target=select_info, args=((i+1),))
        p.start()

    # threads = []    # 多线程
    # for i in range(5):
    #     t1 = threading.Thread(target=select_info, args=(i,))
    #     threads.append(t1)
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # t.join()
