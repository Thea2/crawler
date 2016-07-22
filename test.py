# coding=utf-8
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
#
# driver = webdriver.Firefox()
# driver.get('http://weibo.com/#_loginLayer_%d' % int(time.time() * 1000))
#
# time.sleep(3)
# driver.maximize_window()
#
# driver.find_element_by_name("username").clear()
# driver.find_element_by_name("username").send_keys("13423625046")
#
# driver.find_element_by_name("password").send_keys(Keys.TAB)
# time.sleep(3)
# driver.find_element_by_name("password").send_keys("zhou970713")
#
# driver.find_element_by_name("password").send_keys(Keys.ENTER)
#
# time.sleep(3)
# driver.quit()




# a = map(lambda x: int(x), str(11111111))
# print type(a)


# m = 2
# n = 5
# print reduce( lambda x, y: x * y, range( 1, n + 1 ), m )

# a = [1, 3, 5, 1]
# a.count()
# print a
import re
s = 'gsoigjeosgsi'
p = re.search('g(.*?)gj', s).group(1)
print p
