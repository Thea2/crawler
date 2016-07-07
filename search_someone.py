# coding=utf-8

import re
import urllib2
import Momi
import threading
import multiprocessing

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}
a = Momi.MoblieWeibo()
a.login(13423625046, 'zhou970713')


def search_someone(name, i=0):
    """
    搜索某微博
    :param name:微博名字
    :param i: 根据微博名字所匹配的第i+1个结果
    :return: 微博首页链接
    """
    url = "http://weibo.cn/search/user/?keyword=%s" % name
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    text = response.read()
    id_pattern = re.compile('<tr><td valign="top"><a href="/(.*?)\?f=search_%d"><img' % i)
    pattern = re.compile('.*<tr><td valign="top"><a href="/')
    user_id = re.findall(id_pattern, text)
    user_id = str(user_id)
    if "<tr>" not in user_id:
        return "http://weibo.cn/%s" % user_id[2:-2]
    else:
        user_id = re.sub(pattern, '', user_id)
    return "http://weibo.cn/%s" % user_id[:-2]


def show_content(url):
    """
    输出微博正文
    :param url:微博链接
    :return: 无
    """
    req = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(req)
    text = response.read()
    content_pattern = re.compile('<div class="c".*?<span class="ctt">(.*?)</span>')
    pattern = re.compile('<.*?>')
    content = re.findall(content_pattern, text)
    for x in content:
        x = re.sub(pattern, '', str(x))
        print x
    print "aaaa"

if __name__ == '__main__':
    name = "今日头条"
    # threads = []    # 多线程
    # for i in range(5):
    #     url = search_someone(name, i=i)
    #     print url
    #     t1 = threading.Thread(target=show_content, args=(url,))
    #     threads.append(t1)
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # t.join()
    for i in range(5):    # 多进程
        url = search_someone(name, i=i)
        print url
        p = multiprocessing.Process(target=show_content, args=(url,))
        p.start()