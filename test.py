# coding=utf-8
import urllib2
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}

content_pattern = re.compile('<div class="content">([\w\W]*?)</div>([\w\W]*?)class="stats"')
pattern = re.compile('<.*?>')
url = 'http://www.qiushibaike.com/hot/page/%d/' % 1
request = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(request)
text = response.read()
# print text
# print type(text)
content = re.findall(content_pattern, text)
print content
print type(content)
for x in content:
    if "img" not in x[1]:
        x = re.sub(pattern, '', x[0])
        x = re.sub('\n', '', x)
        print x
    # print x[0]
    # print "aaaa"
    # print x[1]
    # print x