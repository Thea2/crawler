# coding=utf-8
import urllib2
import re
import Momi
import threading

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0'}
a = Momi.MoblieWeibo()
a.login(13423625046, 'zhou970713')


class analysis:
    def __init__(self, keywords):    # 初始化
        self.base_url = 'http://weibo.cn/'
        self.keywords = keywords
        self.file = 'dataSet/analysis_result'
        self.sum_num = 0.0
        self.sex_w = 0
        self.sex_m = 0
        self.sex_other = 0
        self.age_80_before = 0
        self.age_80 = 0
        self.age_90 = 0
        self.age_00 = 0
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
                        if int(age_[0]) >= 2000:
                            self.age_00 += 1
                        elif int(age_[0]) >= 1990:
                            self.age_90 += 1
                        elif int(age_[0]) >= 1980:
                            self.age_80 += 1
                        else:
                            self.age_80_before += 1
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
        f.write('各年龄所占比例：' + '\n'
                + '00后：' + str((self.age_00 / self.sum_num) * 100) + '%' + '\n'
                + '90后：' + str((self.age_90 / self.sum_num) * 100) + '%' + '\n'
                + '80后：' + str((self.age_80 / self.sum_num) * 100) + '%' + '\n'
                + '80后以前：' + str((self.age_80_before / self.sum_num) * 100) + '%' + '\n'
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
        for i in range(100):
            page_num = i + 1
            url = self.base_url + 'search/mblog?keyword=' + self.keywords + '&page=' + str(page_num)
            search_page = self.get_page(url)
            user_info = self.get_user_info(search_page)
            self.collect_user_info(user_info)
            self.count_time(search_page)
            print 'page', i
        self.count_info_result()


if __name__ == '__main__':
    keyword_list = ['友谊的小船说翻就翻', '我要回农村', '城市套路深', '猴赛雷']
    threads = []
    for i in range(len(keyword_list)):
        keyword_analysis = analysis(keyword_list[i])
        t1 = threading.Thread(target=keyword_analysis.start())
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()