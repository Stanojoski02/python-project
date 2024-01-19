#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# I used the project with a facebook account that has no friends, in public groups and despite that sometimes it gave me some error do not forget I am still learning
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#


path = "C:\selenium\chromedriver.exe"


from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import tkinter


def func():
    TIME = int(time_entry.get())
    chrome_options = webdriver.ChromeOptions()
    email = email_entry.get()
    pw = pw_entry.get()
    a = groups_entry.get().split()
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path)
    post = post_entry.get()
    driver.get(a[0])
    time.sleep(1)
#   Login      #
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('pass').send_keys(pw)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div/form/div[2]/div[3]').click()

    while True:
        for i in a:
            driver.get(i)
            time.sleep(6)
            driver.find_element_by_xpath("//*[text()='Write something...']").click()
            time.sleep(2)
            driver.find_element_by_css_selector("div[class = '_1mf _1mj']").send_keys(post)
            time.sleep(2)
            post = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div')
            post.click()
            time.sleep(6)
        time.sleep(TIME)


window = tkinter.Tk()
window.config(pady=20,padx=20)
window.minsize(width=400, height=500)

canvas = tkinter.Canvas(width=200, height=200)
photo = tkinter.PhotoImage(file="img.png")
canvas.create_image(100,100,image=photo)
canvas.grid(column = 1, row=0,columnspan=2,padx=20,pady=20)

email_label = tkinter.Label(text="Email:")
email_label.grid(row=1,column=0, pady=10)
pass_label = tkinter.Label(text="Password:")
pass_label.grid(row=2,column=0,pady=10)
group_label = tkinter.Label(text="Group/s:")
group_label.grid(row=3,column=0,pady=10)
post_label = tkinter.Label(text="Link of post:")
post_label.grid(row=4,column=0,pady=10)
time_label = tkinter.Label(text="Time for posting:")
time_label.grid(row=5,column=0,pady=10,padx=2)

email_entry = tkinter.Entry()
email_entry.grid(column=1,row=1)
pw_entry = tkinter.Entry(show="*")
pw_entry.grid(column=1,row=2)
groups_entry = tkinter.Entry(width=40)
groups_entry.grid(row=3,column=1)
post_entry = tkinter.Entry(width=40)
post_entry.grid(row=4,column=1)
time_entry = tkinter.Entry()
time_entry.grid(row=5,column=1)

start_posting = tkinter.Button(width=12,text="Start Posting!",bg='black',fg='white',command=func)
start_posting.grid(row=6,column=0,pady=10)

window.mainloop()
