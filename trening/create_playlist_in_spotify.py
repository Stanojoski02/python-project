from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import tkinter as tk


def create_playlist(year):
    path = "C:\\Users\\Pc4all\\Downloads\\chromedriver_win32 (3)\\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get(f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/")
    nav = driver.find_element(By.XPATH, '/html/body/div[4]/main/div[2]/div[1]/div/div[2]/div[2]/div[1]/nav')
    nav.click()
    text = driver.find_elements(By.ID, 'title-of-a-story')
    songs = [i.text for i in text if len(i.text.split()) < 6 and len(i.text.split()) > 0]
    indx = songs.index('Follow Us')
    for element in songs[indx:]:
        songs.remove(element)
    print(songs)
    driver.get("https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
    email = ""
    password = ""
    email_element = driver.find_element(By.ID, 'login-username')
    email_element.send_keys(email)
    password_element = driver.find_element(By.ID, "login-password")
    password_element.send_keys(password)
    time.sleep(1)
    login_button = driver.find_element(By.ID, 'login-button')
    login_button.click()
    login_button.click()
    time.sleep(7)
    create_play_list_button = driver.find_element(By.CLASS_NAME, 'IPVjkkhh06nan7aZK7Bx')
    create_play_list_button.click()
    time.sleep(3)
    for song in songs:
        time.sleep(3)
        search_song = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[2]/div[3]/section/div/div/input')
        search_song.clear()
        search_song.send_keys(song)
        time.sleep(2)
        song_to_click = driver.find_element(By.CSS_SELECTOR, 'div[aria-rowindex="1"]')
        song_to_click.click()
        time.sleep(3)
        add = song_to_click.find_element(By.XPATH, "//*[contains(text(), 'Add')]")
        add.click()
        entry.delete()
    time.sleep(20)


window = tk.Tk()
window.config(bg="white")
window.config(padx=50, pady=50, bg="lightblue")

label = tk.Label(text="Create Spotify PlayList\nwith best songs in year", bg="lightblue", font=("Courier", 10, 'bold'), fg="white")
label.grid(column=1, row=0, columnspan=2, padx=10, pady=10)

entry = tk.Entry()
entry.grid(column=1, row=2, columnspan=1)

button = tk.Button(text="Create PlayList", command=lambda: create_playlist(entry.get()))
button.grid(column=2, row=2, columnspan=1, padx=10)

window.mainloop()
