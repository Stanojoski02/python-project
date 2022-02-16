PATH = "c:\selenium\chromedriver.exe"
import tkinter
from selenium import webdriver
import time

driver = webdriver.Chrome(PATH)
driver.set_window_position(-10000,0)

driver.get("https://ytmp3.cc/uu118cc/")


def down():
    input = driver.find_element_by_id("input")
    text = entry.get()
    input.send_keys(text)
    buton = driver.find_element_by_id("submit")
    buton.click()
    time.sleep(8)
    downl = driver.find_element_by_id("download")
    downl.click()
def mp3():
    button = driver.find_element_by_id("mp3")
    button.click()
def mp4():
    button = driver.find_element_by_id("mp4")
    button.click()

#----user interface----#
window = tkinter.Tk()
window.config(bg='gray',pady=20,padx=20)

label = tkinter.Label(text="Which song do you want to download?",fg="white",bg="gray")
label.grid(column=1,row=1,pady=10,columnspan=2)

canvas = tkinter.Canvas()

canvas.config(height=200,width=200,bg="gray")
img = tkinter.PhotoImage(file="img.png")
canvas.create_image(100,100,image=img)
canvas.grid(column=1,row=0,columnspan=2)




entry = tkinter.Entry(width=36)
entry.grid(column=1,row=2,columnspan=2,pady=20)

mp3_button = tkinter.Button(text="MP3",width=14,command=mp3)
mp3_button.grid(column=1,row=3,pady=10)

mp4_button = tkinter.Button(text="MP$",width=14,command=mp4)
mp4_button.grid(column=2,row=3,pady=10)

download = tkinter.Button(text="Download",command=down,width=30)
download.grid(column=1,row=4,columnspan=2)

window.mainloop()
