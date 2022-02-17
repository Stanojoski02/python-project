

# -------------------------The reporter only works with an account that has no followers----------------------#
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
# ------LOGIN-------#
EMAIL = ""
PASSWORD = ""
TARGET = ""

PATH = "c:\selenium\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(4)
username = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
username.send_keys(EMAIL)

password = driver.find_element_by_name("password")
password.send_keys(PASSWORD)

login = driver.find_element_by_css_selector("button[type='submit'")
login.click()
time.sleep(4)
search = driver.find_element_by_css_selector("input[placeholder='Search']")

search.send_keys(TARGET)
time.sleep(1)

search.send_keys(Keys.ENTER)
search.send_keys(Keys.ENTER)
while True:
    time.sleep(4)
    menu = driver.find_element_by_css_selector("button[type='Button'] svg")
    menu.click()
    report = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div/button[3]')
    report.click()
    time.sleep(1)
    report_acc = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/div/div/div/div[3]/button[2]/div/div[1]')
    report_acc.click()
    time.sleep(1)
    wrong_acc = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div/div/div/div[3]/button[1]/div/div[1]")
    wrong_acc.click()
    time.sleep(1)
    dont_like = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/div/div/div/div[3]/button[2]/div/div[1]')
    dont_like.click()
    time.sleep(1)
    close = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div/div/div/div[4]/button')
    close.click()
    # block1 = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/button[1]')
    # block1.click()
