
import tkinter
from tkinter import messagebox
import random
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pww():
    pw_entry.delete(0,"end")
    a=["a","b","c","d","e","f","g","h","x","y"]
    b=["/",".",",","@","&","*",")","("]
    c=["1","2","3","4","5","6","7","8","9","10"]
    random.shuffle(a)
    random.shuffle(b)
    random.shuffle(c)
    z=""
    ll = [a,b,c]
    for ds in range(9):
        sda = random.choice(ll)
        rnm = random.randint(0,6)
        buk =sda[rnm]
        z+=buk
    pw_entry.insert(0,z)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_new_user():
    web = web_entry.get()
    em = email_entry.get()
    pw = pw_entry.get()
    if len(web)==0 or len(em)==0 or len(pw)==0:
        messagebox.showinfo(title="Report!!",message="you must fill your entry!")
    else:
        proba = messagebox.askokcancel(title=web,message=f"{em}\n{pw}")
        if proba:
            with open(file="data.txt",mode="a") as data:
                data.write(f"{web} | {em} | {pw}\n")
                web_entry.delete(0,"end")
                email_entry.delete(0,"end")
                pw_entry.delete(0,"end")

# ---------------------------- UI SETUP ------------------------------- #
pendzere = tkinter.Tk()
pendzere.config(pady=20,padx=20)
pendzere.title("Password Manager")

canvas = tkinter.Canvas()
img = tkinter.PhotoImage(file="logo.png")
canvas.config(width=200,height=200)
canvas.create_image(100,100,image=img)
canvas.grid(column=1,row=0)

lab_web = tkinter.Label(text="Website:")
lab_web.grid(column=0,row=1)
lab_ema = tkinter.Label(text="Email/Username:")
lab_ema.grid(column=0,row=2)
lab_pw=tkinter.Label(text="Password:")
lab_pw.grid(column=0,row=3)

web_entry = tkinter.Entry(width=35)
web_entry.grid(columnspan=2,column=1,row=1)
web_entry.focus()
email_entry = tkinter.Entry(width=35)
email_entry.grid(columnspan=2,column=1,row=2)
email_entry.insert(0,"bojan@gmail.com")
pw_entry = tkinter.Entry(width=17)
pw_entry.grid(column=1,row=3)

pw_button = tkinter.Button(text = "Generate Password", command=generate_pww)
pw_button.grid(column=2,row=3)
add_button = tkinter.Button(width=30,text="Add",command=add_new_user)
add_button.grid(column=1,row=4,columnspan=2)



pendzere.mainloop()
