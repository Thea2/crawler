# coding=utf-8
import urllib2
import re
import Momi
import threading

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}
# a = Momi.MoblieWeibo()
# a.login('gwkus48fei@163.com', 'pachong5')


class analysis(object):
    def __init__(self, keywords, name, password):    # 初始化
        a = Momi.MoblieWeibo()
        a.login(name, password)
        self.base_url = 'http://weibo.cn/'
        self.keywords = keywords
        self.file = 'dataSet/analysis_result'
        self.sum_num = 0.0
        self.sex_w = 0
        self.sex_m = 0
        self.sex_other = 0
        self.age_80_89 = 0
        self.age_79 = 0
        self.age_90_94 = 0
        self.age_95 = 0
        self.age_other = 0
        self.area_list = ['其他', '北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西',
                          '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '广西', '内蒙古',
                          '西藏', '宁夏', '新疆', '香港', '澳门']
        self.area_num = [0] * len(self.area_list)
        self.time_list = ['2016年7月', '2016年6月', '2016年5月', '2016年4月', '2016年3月', '2016年2月', '2016年1月',
                          '2015年12月', '2015年11月', '2015年10月', '2015年9月', '2015年8月', '2015年7月',
                          '2015年6月', '2015年5月', '2015年4月', '2015年3月', '2015年2月', '2015年1月',
                          '2014年12月', '2014年11月', '2014年10月', '2014年9月', '2014年8月', '2014年7月',
                          '2014年6月', '2014年5月', '2014年4月', '2014年3月', '2014年2月', '2014年1月',
                          '2013年12月', '2013年11月', '2013年10月', '2013年9月', '2013年8月', '2013年7月',
                          '2013年6月', '2013年5月', '2013年4月', '2013年3月', '2013年2月', '2013年1月']
        self.time = {'2016年7月': {'starttime': '20160701', 'endtime': '20160731'},
                     '2016年6月': {'starttime': '20160601', 'endtime': '20160631'},
                     '2016年5月': {'starttime': '20160501', 'endtime': '20160531'},
                     '2016年4月': {'starttime': '20160401', 'endtime': '20160431'},
                     '2016年3月': {'starttime': '20160301', 'endtime': '20160331'},
                     '2016年2月': {'starttime': '20160201', 'endtime': '20160231'},
                     '2016年1月': {'starttime': '20160101', 'endtime': '20160131'},
                     '2015年12月': {'starttime': '20151201', 'endtime': '20151231'},
                     '2015年11月': {'starttime': '20151101', 'endtime': '20151131'},
                     '2015年10月': {'starttime': '20151001', 'endtime': '20151031'},
                     '2015年9月': {'starttime': '20150901', 'endtime': '20150931'},
                     '2015年8月': {'starttime': '20150801', 'endtime': '20150831'},
                     '2015年7月': {'starttime': '20150701', 'endtime': '20150731'},
                     '2015年6月': {'starttime': '20150601', 'endtime': '20150631'},
                     '2015年5月': {'starttime': '20150501', 'endtime': '20150531'},
                     '2015年4月': {'starttime': '20150401', 'endtime': '20150431'},
                     '2015年3月': {'starttime': '20150301', 'endtime': '20150331'},
                     '2015年2月': {'starttime': '20150201', 'endtime': '20150231'},
                     '2015年1月': {'starttime': '20150101', 'endtime': '20150131'},
                     '2014年12月': {'starttime': '20141201', 'endtime': '20141231'},
                     '2014年11月': {'starttime': '20141101', 'endtime': '20141131'},
                     '2014年10月': {'starttime': '20141001', 'endtime': '20141031'},
                     '2014年9月': {'starttime': '20140901', 'endtime': '20140931'},
                     '2014年8月': {'starttime': '20140801', 'endtime': '20140831'},
                     '2014年7月': {'starttime': '20140701', 'endtime': '20140731'},
                     '2014年6月': {'starttime': '20140601', 'endtime': '20140631'},
                     '2014年5月': {'starttime': '20140501', 'endtime': '20140531'},
                     '2014年4月': {'starttime': '20140401', 'endtime': '20140431'},
                     '2014年3月': {'starttime': '20140301', 'endtime': '20140331'},
                     '2014年2月': {'starttime': '20140201', 'endtime': '20140231'},
                     '2014年1月': {'starttime': '20140101', 'endtime': '20140131'},
                     '2013年12月': {'starttime': '20131201', 'endtime': '20131231'},
                     '2013年11月': {'starttime': '20131101', 'endtime': '20131131'},
                     '2013年10月': {'starttime': '20131001', 'endtime': '20131031'},
                     '2013年9月': {'starttime': '20130901', 'endtime': '20130931'},
                     '2013年8月': {'starttime': '20130801', 'endtime': '20130831'},
                     '2013年7月': {'starttime': '20130701', 'endtime': '20130731'},
                     '2013年6月': {'starttime': '20130601', 'endtime': '20130631'},
                     '2013年5月': {'starttime': '20130501', 'endtime': '20130531'},
                     '2013年4月': {'starttime': '20130401', 'endtime': '20130431'},
                     '2013年3月': {'starttime': '20130301', 'endtime': '20130331'},
                     '2013年2月': {'starttime': '20130201', 'endtime': '20130231'},
                     '2013年1月': {'starttime': '20130101', 'endtime': '20130131'}}
        self.time_num = [0] * len(self.time_list)

    def get_page(self, url):
        """
        获取网页的源代码
        :param url: 该网页的链接
        :return: 网页的源代码
        """
        try:
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None

    def get_user_info(self, search_page):
        """
        获取用户资料
        :param search_page:搜索结果网页源代码
        :return: 用户资料列表
        """
        user_info = []
        id_pattern = re.compile('uid=(\d*)&amp;rl=1#cmtfrm" class="cc">评论')
        user_id = re.findall(id_pattern, search_page)    # 获取用户id
        for uid in user_id:     # 进入用户资料界面，爬取用户资料
            link = self.base_url + str(uid) + '/info'
            user_page = self.get_page(link)
            info_pattern = re.compile('<div class="tip">基本信息</div><div class="c">(.*?)</div>')
            info = re.findall(info_pattern, user_page)
            for x in info:
                user_info.append(x)
                print 'info', x
        return user_info

    def count_time(self, search_page):
        """
        统计博文发布时间
        :param search_page: 搜索结果页面源代码
        """
        time_pattern = re.compile('收藏</a><!---->&nbsp;<span class="ct">(.*?)&nbsp;')
        time_list = re.findall(time_pattern, search_page)
        month_list = ['07月', '06月', '05月', '04月', '03月', '02月', '01月']
        for time in time_list:
            if '分钟前' in time:
                self.time_num[0] += 1
            elif '今天' in time:
                self.time_num[0] += 1
            else:
                num = 0
                for j in range(24):
                    if self.time_list[j+7] in time:
                        self.time_num[j+7] += 1
                        num += 1
                        break
                if num == 0:
                    for i in range(len(month_list)):
                        if month_list[i] in time:
                            self.time_num[i] += 1
                            break

    def collect_user_info(self, user_info):
        """
        统计用户信息
        :param user_info:用户资料列表
        """
        self.sum_num += len(user_info)
        sex_pattern = re.compile('性别:(.*?)<br/>')
        age_pattern = re.compile('生日:(\d*)-(\d*)-(\d*)<br/>')
        area_pattern = re.compile('地区:(.*?)<br/>')
        for info in user_info:
            sex = re.findall(sex_pattern, info)
            age = re.findall(age_pattern, info)
            area = re.findall(area_pattern, info)
            if sex:     # 用户性别统计
                if '男' in sex:
                    self.sex_m += 1
                elif '女' in sex:
                    self.sex_w += 1
                else:
                    self.sex_other += 1
            else:
                self.sex_other += 1
            if age:    # 用户年龄段的统计
                for age_ in age:
                    if age:
                        if int(age_[0]) == 0001:
                            self.age_other += 1
                        elif int(age_[0]) >= 1995:
                            self.age_79 += 1
                        elif int(age_[0]) >= 1990:
                            self.age_80_89 += 1
                        elif int(age_[0]) >= 1980:
                            self.age_90_94 += 1
                        else:
                            self.age_95 += 1
                    else:
                        self.age_other += 1
            else:
                self.age_other += 1
            if area:     # 用户所属地区的统计
                for area_ in area:
                    num = 0
                    for i in range(len(self.area_list)):
                        if self.area_list[i] in area_:
                            self.area_num[i] += 1
                            num += 1
                            break
                    if num == 0:
                        self.area_num[0] += 1
            else:
                self.area_num[0] += 1

    def count_info_result(self):    # 将相关用户信息的统计结果写入文件
        f = open(self.file, 'a')
        f.write(self.keywords + '\n')
        f.write('各年龄段所占比例：' + '\n'
                + '95～：' + str((self.age_79 / self.sum_num) * 100) + '%' + '\n'
                + '90-94：' + str((self.age_80_89 / self.sum_num) * 100) + '%' + '\n'
                + '80-89：' + str((self.age_90_94 / self.sum_num) * 100) + '%' + '\n'
                + '~79：' + str((self.age_95 / self.sum_num) * 100) + '%' + '\n'
                + '其他：' + str((self.age_other / self.sum_num) * 100) + '%' + '\n')
        f.write('各性别所占比例：' + '\n'
                + '男：' + str((self.sex_m / self.sum_num) * 100) + '%' + '\n'
                + '女：' + str((self.sex_w / self.sum_num) * 100) + '%' + '\n'
                + '其他：' + str((self.sex_other / self.sum_num) * 100) + '%' + '\n')
        f.write('各省份所占比例：' + '\n')
        for i in range(len(self.area_list)):
            f.write(self.area_list[i] + '：' + str((self.area_num[i] / self.sum_num) * 100) + '%' + '\n')
        f.write('使用时间频率分布：'+'\n')
        for j in range(len(self.time_list)):
            f.write(self.time_list[j]+'：'+str((self.time_num[j]/self.sum_num)*100)+'%'+'\n')
        f.close()

    def start(self):
        for j in range(len(self.time_list)):
            for i in range(100):
                page_num = i + 1
                url = self.base_url + 'search/mblog?keyword=' + self.keywords + '&starttime=' + self.time[self.time_list[j]]['starttime']\
                      + '&endtime=' + self.time[self.time_list[j]]['endtime'] + '&page=' + str(page_num)
                search_page = self.get_page(url)
                user_info = self.get_user_info(search_page)
                self.collect_user_info(user_info)
                self.time_num[j] += len(user_info)
                # self.count_time(search_page)
                print 'page', i
            print 'time', j
        self.count_info_result()


if __name__ == '__main__':
    keyword_list = ['友谊的小船说翻就翻', '我要回农村', '城市套路深', '猴赛雷']
    user_list = ['zpyan315fu@163.com', 'gzmaov96jing@163.com', 'rsba313shao@163.com', 'yowjingk26shi@163.com', 'gwkus48fei@163.com']
    password_list = ['pachong1', 'pachong2', 'pachong3', 'pachong4', 'pachong5']
    threads = []
    for i in range(len(keyword_list)):
        keyword_analysis = analysis(keyword_list[i], user_list[i], password_list[i])
        t1 = threading.Thread(target=keyword_analysis.start())
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    # analysis(keyword_list[0], user_list[0], password_list[0]).start()
    # analysis(keyword_list[1], user_list[1], password_list[1]).start()
    # analysis(keyword_list[2], user_list[2], password_list[2]).start()
    # analysis(keyword_list[3], user_list[3], password_list[3]).start()