import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import csv
import pandas
c=0

# Regex is used to recognize the email address in source page
REGEX = r'''([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?(\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)+'''

# Path to chromedriver
path ="c:\selenium\chromedriver.exe"
# urls from which data should be collected
url = ["https://github.com",'https://youtube.com','https://www.randomlists.com/email-addresses',"https://stackoverflow.com/","https://github.com"]
driver = webdriver.Chrome(path)
old_data = []

for i in url:
    if i in old_data:
        print(f"{url[c]} data is already stored")
    else:
        old_data.append(url[c])
        driver.get(i)
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR,"button[class='flex--item s-btn s-btn__primary js-accept-cookies js-consent-banner-hide']").click()
        except:
            pass
        try:
            logo = driver.find_element(By.CSS_SELECTOR, "link[rel='icon']")
            logo = str(logo.get_attribute("href"))
        except:
            logo = "empty"
        try:
            description = driver.find_element(By.CSS_SELECTOR,"meta[name='description']")
            description = str(description.get_attribute("content"))
        except:
            description = "empty"
        try:
            title = driver.title
        except:
            title = "empty"
        page_source = driver.page_source
        emails = []
        try:
            for i in re.finditer(REGEX,page_source):
                emails.append(i.group())
        except:
            emails = ["Empty"]
        f = "Website url,title,description,logo,email"
        with open("data.csv", "a",encoding="UTF-8") as d:
            thewriter=csv.writer(d)
            thewriter.writerow([f"'{url[c]}'",f"'{title}'",f"'{description}'",f"'{logo}'",f"'{emails}'"])
            print(f"Data of {url[c]} is saved!")
            c+=1
driver.close()

question = input("Data collection is complete if you want to view the data press y")
if question == "y":
    sl = pandas.read_csv("data.csv")
    print(sl)

