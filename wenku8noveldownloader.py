from selenium import webdriver
import cloudscraper
import os
import time

# 设置Selenium
browser = webdriver.Chrome()

# 打开登录页面
LOGIN_URL = "https://www.wenku8.net/login.php"  # 替换为你的登录URL
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

# 定义保存目录
SAVE_DIR = r"C:\wenku2"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def download_txt(num):
    url = f"https://dl1.wenku8.com/down/txtutf8/2/{num}.txt"
    response = scraper.get(url)
    
    if response.status_code == 200:
        with open(os.path.join(SAVE_DIR, f"{num}.txt"), "wb") as f:
            f.write(response.content)  # 保存为UTF-8编码
        print(f"Downloaded {num}.txt successfully!")
    else:
        print(f"Failed to download {num}.txt. Status code: {response.status_code}")

# 下载文件
for i in range(2000, 3005):
    download_txt(i)
    time.sleep(5)  # 每5秒下载一个

