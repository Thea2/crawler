# coding=utf-8

import urllib2
import re
import Momi
import threading
import semantic.key_score as key_extraction
import semantic.calculate_Similarity as judge_similarity

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}


class GetNews:    # 获取某媒体热点新闻的类

    def __init__(self, baseURL, media, uid, page_num):
        """
        初始化
        :param baseURL:基本链接
        :param uid: 该媒体的用户id
        :param page_num: 获取媒体前几页的热点新闻
        """
        self.baseURL = baseURL
        self.uid = uid
        self.file_name = 'dataSet/%s.txt' % media
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
        link_pattern = re.compile('http:.*?')
        content = re.findall(content_pattern, page)
        for x in content:
            if (x[1] > 20) and (x[2] > 50) and (x[3] > 20):    # x[0]为微博正文，x[1]为该博文赞的数量，x[2]为该博文转发的数量，x[3]为该博文评论的数量
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
                        new = re.sub(link_pattern, '', new)
                else:
                    new = re.sub(pattern, '', x[0])
                    new = re.sub(link_pattern, '', new)
                news.append(new)
                print new
        return news

    def save_data(self, new):    # 将热点新闻存入指定文件
        f = open(self.file_name, 'r')
        if new not in f.read():
            ff = open(self.file_name, 'a')
            ff.write(new + '\n')
            ff.close()
        f.close()

    def start(self):    # 开始工作～
        for i in range(int(self.page_num)):
            page = self.get_page(i + 1)
            news = self.get_new_content(page)
            for new in news:
                self.save_data(new)


class Judger(object):   # 判断热点新闻的类

    def __init__(self, media_list):
        """
        初始化
        :param media_list:媒体列表
        """
        self.media_list = media_list

    def keyword_extract(self, news_file):
        """
        关键词提取
        :param news_file:储存新闻的文档
        :return: 新闻的关键词列表
        """
        new_keyword_list = []
        f = open(news_file, 'r')
        r = f.readline()
        while r:   # 提取每条新闻的关键词并加入关键词列表
            keyword = ''
            keyword_list = key_extraction.Keyword().keyword(r)[0]
            tag = 1
            for key in keyword_list:
                keyword += key
                if tag > 4:     # 只取权重为前4的关键词
                    break
                tag += 1
            if keyword:
                new_keyword_list.append(keyword)
            r = f.readline()
        return new_keyword_list

    def judge_hot_news(self, new_keywords_lists):
        """
        判断新闻在多家媒体中是否为热点新闻
        :param new_keywords_lists: 由多家媒体的关键词列表构成的列表
        :return: 热点新闻的媒体的位置和对应的新闻的位置的列表
        """
        num = len(new_keywords_lists)
        # print 'new_keywords_list', new_keywords_lists
        hot_news = []
        for i in range(num):
            for new in new_keywords_lists[i]:    # 把每家媒体的新闻关键词与其他家媒体的关键词进行相似度匹配
                j = 0
                similar_num = 0
                while j < num:
                    if i == j:
                        j += 1
                        continue
                    for other_new in new_keywords_lists[j]:
                        # print judge_similarity.TextAnalyse().similay(new, other_new)
                        if judge_similarity.TextAnalyse().similay(new, other_new) > 0.5:    # 相似度大于0.5则认为两条新闻相同
                            similar_num += 1
                            print new, other_new
                    if similar_num > 1:   # 有一家以上媒体报道相同的新闻则认为该新闻为热点新闻
                        if [i, new_keywords_lists[i].index(new)] not in hot_news:
                            hot_news.append([i, new_keywords_lists[i].index(new)])
                    j += 1
        print 'hot_news_list', hot_news
        return hot_news

    def show_hot_new(self, hot_news):
        """
        展示热点新闻
        :param hot_news: 热点新闻的媒体的位置和对应的新闻的位置的列表
        """
        for each in hot_news:
            f = open('dataSet/%s.txt' % self.media_list[int(each[0])])
            tag = 0
            r = f.readline()
            while 1:
                if int(each[1]) == tag:
                    print self.media_list[int(each[0])], r
                    break
                else:
                    tag += 1
                    r = f.readline()

    def run(self):
        new_key__lists = []
        for media in self.media_list:
            key_list = self.keyword_extract('dataSet/%s.txt' % media)
            new_key__lists.append(key_list)
        hot_new_list = self.judge_hot_news(new_key__lists)
        self.show_hot_new(hot_new_list)


if __name__ == '__main__':
    a = Momi.MoblieWeibo()
    a.login('oktong668an@163.com', 'pachong13')
    base_url = 'http://weibo.cn/'
    media = {
        'jinritoutiao': '2745813247',
        'sohu': '2083844833',
        'wangyi': '1974808274',
        'fenghuang': '1992613670',
        'yangshi':  '2656274875'
    }
    threads = []
    for m in media:
        get_news = GetNews(base_url, m, media[m], 2)
        t1 = threading.Thread(target=get_news.start())
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    media_list = media.keys()
    Judger(media_list).run()
