from tkinter import messagebox
import tkinter
import screen2
import json
from twilio.rest import Client
import requests


def for_pw():
    try:
        accaunt_sid = "AC9f6c9bassss1c6bb3d9ae9f"
        auth = "5623bed8437c8b765186e5685324337f"
        from_phone = "+15075sadsa9"
        client = Client(accaunt_sid,auth)
        user = user_entry.get()
        if not user:
            messagebox.showinfo(title="Info",message="User not found please try again")
        else:
            with open("data.json","r") as dat:
                data = json.load(dat)
                pw = data[user]["password"]
            message = client.messages.create(to="+389sss3", from_=from_phone, body=f"Your password is /{pw}/ ")
            messagebox.showinfo(Title="Info",message="Check your messages and find your password")
    except:
        messagebox.showinfo(title="Info", message="User not found please try again")
        password_entry.delete(0,"end")
        user_entry.delete(0,"end")



def add_new_user():
    b.destroy()
    screen2.Screen2()

def naj():
    global a
    user = user_entry.get()
    a = user
    pw = password_entry.get()
    try:
        with open("data.json", "r") as data:
            dataa = json.load(data)
            print(dataa)
            try:
                if dataa[user]:
                    if dataa[user]["password"] == pw:
                        b.destroy()
                        screen2.Screen1(user)
                    else:
                        messagebox.showinfo(message="Wrong password")
                        user_entry.delete(0,"end")
                        password_entry.delete(0,"end")
            except:
                user_entry.delete(0, "end")
                password_entry.delete(0, "end")
                messagebox.showinfo(title="Info!", message="User dont found!")
    except:
        messagebox.showinfo(title="Info!",message="User dont found!")



b = tkinter.Tk()
a = ""
b.config(pady=20,padx=50,bg="lightblue")

user_label = tkinter.Label(text="UserName: ",bg="lightblue",fg="white",font = ('Helvetica', 9, 'bold'))
user_label.grid(column = 0,row=0,pady=10,padx=20)

user_entry = tkinter.Entry()
user_entry.grid(column=1,row=0,pady=20,padx=20)

password_label = tkinter.Label(text="Password: ",bg="lightblue",fg="white",font = ('Helvetica', 9, 'bold'))
password_label.grid(column=0,row=1,pady=10,padx=20)

password_entry = tkinter.Entry(show="*")
password_entry.grid(column=1, row=1,pady=10,padx=20)

najavise = tkinter.Button(text="Login",width=31,command=naj)
najavise.grid(column=0,row=2,columnspan=2,pady=12,padx=20)
banking_systemm = tkinter.Label(text="______________",bg="lightblue",fg="white",font = ('Helvetica', 9, 'bold'))
banking_systemm.grid(column=0,row=5,columnspan=3,pady=10,padx=20)
banking_system = tkinter.Label(text="| Banking system |",bg="lightblue",fg="white",font = ('Helvetica', 9, 'bold'))
banking_system.grid(column=0,row=6,columnspan=3,pady=20,padx=20)

new_user = tkinter.Button(text="New user:",command=add_new_user)
new_user.grid(row=4,column=0,pady=10)

forgot_password = tkinter.Button(text="Forgot Password",width=31,command=for_pw)
forgot_password.grid(row=3,column=0,columnspan=2)

b.mainloop()
