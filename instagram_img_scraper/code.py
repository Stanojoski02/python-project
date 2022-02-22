PATH = "c:\selenium\chromedriver.exe"
USERNAME = ''
PASSWORD = ''
TARGET = ''

import wget
import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(PATH)
driver.get('https://www.instagram.com/')
time.sleep(3)

username = driver.find_element_by_name("username").send_keys(USERNAME)
password = driver.find_element_by_name('password').send_keys(PASSWORD)
login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
time.sleep(4)

search = driver.find_element_by_css_selector("input[placeholder='Search']")
search.send_keys(TARGET)
time.sleep(1)
search.send_keys(Keys.ENTER)
search.send_keys(Keys.ENTER)
time.sleep(4)
driver.execute_script("window.scrollTo(0,4000);")
images = driver.find_elements_by_tag_name("img")
images = [image.get_attribute('src') for image in images]
print(images)

path = os.getcwd()
path = os.path.join(path, "images")
os.mkdir(path)
print(path)

c =0
for i in images:
    save = os.path.join(path, f"img{c}.jpg")
    wget.download(i, save)
    c+=1
