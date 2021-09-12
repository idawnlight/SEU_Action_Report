# coding: utf-8
# Author：quzard
from selenium import webdriver
import random
import time
import datetime
from pytz import timezone
import os
import sys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)

if "ID" in os.environ:
    username = os.environ["ID"]
else:
    print("未找到 ID")
    sys.exit(1)

if "PASSWORD" in os.environ:
    password = os.environ["PASSWORD"]
else:
    print("未找到 PASSWORD")
    sys.exit(1)

t1 = 30
t2 = 5


def main():
    date_time = datetime.datetime.now(tz = timezone('Asia/Shanghai')).strftime("%Y-%m-%d, %H:%M:%S")
    print("开始体温上报 @" + date_time)

    print("尝试登录...")
    login()

    print("打开表单")
    open_form()

    print("新增数据")
    fill_form()


def login():
    # Amazingly, ehall of seu doesn't support https
    # using https will get a 404 error
    url = "http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/index.do#/dailyReport"
    driver.get(url)
    time.sleep(t1)

    checkUrl = driver.current_url
    if checkUrl.startswith("https://newids.seu.edu.cn/"):
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="casLoginForm"]//button[@type="submit"]').click()
    else:
        fail("未知的登录页")
    time.sleep(t1)

    checkUrl = driver.current_url
    if not checkUrl.startswith("http://ehall.seu.edu.cn/"):
        fail("登录失败")

    print("登录成功")


def open_form():
    driver.find_element_by_xpath('//div[@data-action="add"]').click()
    time.sleep(t1)

    if '今日已填报' in driver.page_source:
        success('今日已填报')
    elif '每日健康申报截止' in driver.page_source | '请在此时间内填报' in driver.page_source:
        fail('不在健康申报时间内')


def fill_form():
    temperature = round(random.uniform(36.3, 36.8), 1)

    print("输入体温 " + str(temperature))

    # TODO: better xpath
    if "English Name" in driver.page_source:
        driver.find_element_by_xpath(
            '/html/body/div[11]/div/div[1]/section/div[2]/div/div[3]/div[2]/div[8]/div[1]/div/input').send_keys(
            temperature)
    else:
        driver.find_element_by_xpath(
            '/html/body/div[11]/div/div[1]/section/div[2]/div/div[4]/div[2]/div[1]/div[1]/div/input').send_keys(
            temperature)
    time.sleep(t2)

    div = driver.find_element_by_xpath('//*[@id="save"]')
    # 将下拉滑动条滑动到当前 div 区域
    driver.execute_script("arguments[0].scrollIntoView();", div)
    time.sleep(t2)

    driver.find_element_by_xpath('//*[@id="save"]').click()
    print("点击保存")
    time.sleep(t1)
    if "确定数据无误并提交数据" in driver.page_source:
        # TODO: better xpath
        driver.find_element_by_xpath('/html/body/div[62]/div[1]/div[1]/div[2]/div[2]/a[1]').click()
        success('体温上报成功')
    else:
        fail('请主动上报一次，来完善新增信息')


def success(msg):
    print(msg)
    driver.quit()
    sys.exit(0)


def fail(msg):
    print(msg)
    driver.quit()
    sys.exit(1)


if __name__ == "__main__":
    main()
