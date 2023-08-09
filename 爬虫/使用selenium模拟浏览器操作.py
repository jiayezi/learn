from selenium import webdriver
import time

# browser = webdriver.Chrome()
# url = 'https://www.baidu.com'
# 访问网站
# browser.get(url)

# 获取网页源码
# content = browser.page_source
# print(content)

# 通过xpath路径定位元素
# button = browser.find_element(by="xpath", value='//*[@id="su"]')
# print(button)
# 通过id属性定位元素
# button = browser.find_element(by="id", value='su')
# print(button)

# 获取元素的某个属性的值，比如获取value的值
# button = browser.find_element(by="id", value='su')
# print(button.get_attribute('value'))
# 获取元素的标签名
# button = browser.find_element(by="id", value='su')
# print(button.tag_name)
# 获取元素标之间的文本
# a = browser.find_element(by="name", value='tj_briicon')
# print(a.text)

# # 交互
# input_element = browser.find_element(by="id", value='kw')
# # 向元素传入文字
# input_element.send_keys('python')
# button = browser.find_element(by="id", value='su')
# # 模拟点击按钮
# button.click()
# time.sleep(2)
# # 滚动页面
# # browser.execute('document.documentElement.scrollTop=100000')
# browser.execute_script('window.scrollBy(0,10000)')
# n = browser.find_element(by="xpath", value='//*[@id="page"]/div/a[10]')
# n.click()
# time.sleep(2)
# # 返回
# browser.back()
# time.sleep(2)
# # 前进
# browser.forward()
# # 退出
# browser.quit()

# 无界面启动
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)
url = 'https://www.baidu.com'
browser.get(url)
browser.save_screenshot('0.png')
input()
