from selenium import webdriver
import cloudscraper
import os
import time
from bs4 import BeautifulSoup
import json
import re 
# 设置Selenium
browser = webdriver.Chrome()

# 打开登录页面
LOGIN_URL = "https://www.wenku8.net/login.php"
browser.get(LOGIN_URL)

# 手动登录并验证CloudFlare
input("After logging in and passing CloudFlare, press Enter to continue...")

# 获取cookies
cookies = browser.get_cookies()

# 关闭Selenium session
browser.quit()
# 使用cloudscraper设置
scraper = cloudscraper.create_scraper()

# 设置从Selenium获取的cookies
for cookie in cookies:
    scraper.cookies.set(cookie['name'], cookie['value'])

output_jsons=r'd:\novelinfo'

# 确保一个输出目录存在来保存所有的json文件
if not os.path.exists("output_jsons"):
    os.makedirs("output_jsons")

# 遍历URL
for i in range(3501, 3537):
    url = f"https://www.wenku8.net/book/{i}.htm"
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    print(i)
    # 获取title
    title = soup.title.string.split(" - ")[0]

    # 获取tags
    tag_element = soup.find("span", class_="hottext", string=re.compile("作品Tags"))
    if tag_element:
      tag_string = tag_element.b.string
    if "作品Tags：" in tag_string:
        tags = tag_string.split("作品Tags：")[1].strip().split(' ')

    # 获取description
    desc_element = soup.find("span", string="内容简介：")
    if desc_element and desc_element.find_next("span", style="font-size:14px;"):
      description = desc_element.find_next("span", style="font-size:14px;").text.strip()
    else:
      description = ""

    # 构建数据字典
    data = {
        "novelid": str(i),
        "conversations": [{
            "title": title,
            "tags": " ".join(tags),
            "description": description
        }]
    }

    # 保存为JSON文件
    with open(os.path.join("output_jsons", f"{i}.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 等待3秒
    time.sleep(3)
