PATH = "c:\selenium\chromedriver.exe"
from selenium import webdriver
import time


# The project is not completely completed
# The project is not completely completed
# The project is not completely completed
# The project is not completely completed

driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=103420483&keywords=python%20developer&location=&sortBy=R")
time.sleep(1)

# ----------------login-------------------------c
join = driver.find_element_by_xpath("/html/body/div[1]/header/nav/div/a[2]")
join.click()
time.sleep(2)
email = driver.find_element_by_name("session_key")
email.send_keys("")
password = driver.find_element_by_name("session_password")
password.send_keys("")
time.sleep(1)
login = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
login.click()

jobs = driver.find_elements_by_css_selector(".job-card-container")
for i in jobs:
    if i == jobs[0]:
        pass
    else:
        try:
            i.click()
            time.sleep(3)
            aplay_buton = driver.find_element_by_css_selector(".jobs-apply-button--top-card button")
            aplay_buton.click()
            time.sleep(2)
            number = driver.find_element_by_css_selector('.display-flex input')
            number.send_keys("12334566")
            time.sleep(1)
            try:
                submit = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/form/footer/div[3]/button/span')
                submit.click()
            except:
                next = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/form/footer/div[2]/button/span')
                next.click()
                time.sleep(1)
                home = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/form/div/div/div[1]/div/div/div/div/div[1]/div/input')
                home.send_keys("Prilep")
                next = driver.find_element_by_xpath('//*[@id="ember360"]')
                next.click()
            time.sleep(1)
            close = driver.find_element_by_xpath("/html/body/div[3]/div/div/button/li-icon/svg")
            close.click()
            time.sleep(2)
        except:
            continue





