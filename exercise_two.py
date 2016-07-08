# coding=utf-8
import urllib2
import re


class get_info:      # 获取百度贴吧信息
    def __init__(self, baseUrl, seeLZ):
        """
        初始化
        :param baseUrl:基本链接
        :param seeLZ:是否只看楼主
        """
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)

    def get_page(self, page_num):
        """
        获取网页源代码
        :param page_num:目标网页为第几页
        :return:网页源代码
        """
        try:
            url = self.baseURL+self.seeLZ+'&pn='+str(page_num)    # 基本链接加上是否只看楼主和查看第几页的相关信息组成具体链接
            # print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    def get_content(self, page):
        """
        获取贴吧内容并输入
        :param page:网页源代码
        :return:贴吧选定内容
        """
        content_pattern = re.compile('<cc>(.*?)</cc>')
        pattern = re.compile('<.*?>')
        content = re.findall(content_pattern, page)
        for x in content:
            x = re.sub(pattern, '', x)
            print x.strip()
            print "--------"
        return content

    def start(self):
        num = raw_input("输入查看页数：")
        for i in range(int(num)):
            page = self.get_page(i+1)
            self.get_content(page)
1

if __name__ == '__main__':
    baseURL = 'http://tieba.baidu.com/p/3138733512'
    seeLZ = raw_input("若只获取楼主发言请输入1，否则请输入0")
    tieba_content = get_info(baseURL, seeLZ)
    tieba_content.start()