# coding=utf-8
import urllib2
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}


def get_content():
    """
    从糗事百科中获取故事
    :return: 故事列表
    """
    stories = []
    content_pattern = re.compile('<div class="content">([\w\W]*?)</div>([\w\W]*?)class="stats"')
    pattern = re.compile('<.*?>')
    for i in range(20):    # 爬取糗事百科前20页的故事并存入故事列表
        url = 'http://www.qiushibaike.com/hot/page/%d/' % (i+1)
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            text = response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
        content = re.findall(content_pattern, text)
        for x in content:
            if "img" not in x[1]:
                x = re.sub(pattern, '', x[0])
                x = re.sub('\n', '', x)
                stories.append(x)

    return stories


def show_stories(stories):
    """
    逐一展示故事
    :param stories:故事列表
    :return: 无
    """
    for story in stories:
        input_ = raw_input("查看故事请按回车，退出请按Q")
        if input_ == "Q":
            break
        print story
    print "end"

if __name__ == '__main__':
    stories = get_content()
    show_stories(stories)