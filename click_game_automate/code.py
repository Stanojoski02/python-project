from selenium import webdriver
chrome_driver_path = "c:\selenium\chromedriver.exe"
from selenium import webdriver
import time

driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
click_button = driver.find_element_by_id("cookie")
by_grand = driver.find_element_by_id("buyGrandma")
items = driver.find_elements_by_css_selector("#store div")
a = []
for i in items:
    a.append(i.text)
baka = a[1].splitlines()[0].split()[2]

fabrika = a[2].splitlines()[0].split()[2]

print(fabrika)

while True:
    money = driver.find_element_by_id("money")
    try:
        if int(money.text) > 500:
            by_fabrika = driver.find_element_by_id("buyFactory")
            by_fabrika.click()
        else:
            by_grand = driver.find_element_by_id("buyGrandma")
            try:
                by_fabrika = driver.find_elements_by_id("buyFactory")
            except:
                continue
            for i in range(110):
                click_button.click()
            money = driver.find_element_by_id("money")
            items = driver.find_elements_by_css_selector("#store div")

            a = []
            for i in items:
                a.append(i.text)
            baka = a[1].splitlines()[0].split()[2]

            if int(baka)<int(money.text):
                try:
                    by_grand.click()
                except:
                    continue
    except:
        continue




