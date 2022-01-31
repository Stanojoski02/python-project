from tkinter import Tk
import tkinter
import json
from tkinter import messagebox

class new_pw_screen:
    def __init__(self,user):
        self.window = tkinter.Tk()
        self.window.config(bg="lightblue")
        self.user = user
        self.window.config(pady=20,padx=20)
        self.new_pw_label = tkinter.Label(text="New password")
        self.new_pw_label.grid(column=0,row=0,pady=10,padx=10)
        self.new_pw_entry = tkinter.Entry()
        self.new_pw_entry.grid(column=1,row=0,pady=10,padx=10)
        self.button = tkinter.Button(text = "Add Password",width=30,command=self.add_pw)
        self.button.grid(column=0,row=1,columnspan=2,pady=10,padx=10)
        self.window.mainloop()
    def add_pw(self):
        pw = self.new_pw_entry.get()
        user = self.user
        with open("data.json","r") as dat:
            data = json.load(dat)
            data[user]["password"] = pw
        with open("data.json","w") as datt:
            json.dump(data,datt,indent=4)
            self.new_pw_entry.delete(0,"end")
        self.window.destroy()
        Screen1(self.user)



class Screen1(Tk):
    def __init__(self,user):
        super().__init__()

        self.user = user
        self.balance = 0
        self.balance_label = tkinter.Label(text="Your balance: ",bg="white",fg="black",width=17)
        self.balance_label.grid(row=0,column=1,columnspan=2,pady=20,padx=6)
        self.config(width=500,height=500,pady=50,padx=50,bg="lightblue")
        label = tkinter.Label(text="Enter the amount of money",fg="black",bg="white")
        label.grid(column=1,row=1,columnspan=2,pady=20,padx=6)
        self.entry=tkinter.Entry()
        self.entry.grid(row=2,column=1,columnspan=2,pady=20,padx=6)
        vnes_pari = tkinter.Button(text = "Vnesi pari!",fg="black",bg="white",command=self.add_money)
        vnes_pari.grid(column=1,row=3,pady=20,padx=6)
        podigni_pari = tkinter.Button(text="Povleci pari!",fg="black",bg="white",command=self.get_moneyy)
        podigni_pari.grid(column=2,row=3,pady=20,padx=6)
        self.balance_button = tkinter.Button(text = "Balance",width=20,bg="white",fg="black",command=self.see_balance)
        self.balance_button.grid(column=1,row=4,columnspan=2,pady=20,padx=6)

        self.send_money_label = tkinter.Label(text = "Send money to:",bg="white",fg="black")
        self.send_money_label.grid(row = 0,column=3,padx=10)

        self.money = tkinter.Label(text="Amount:",bg="white",fg="black")
        self.money.grid(row=1,column=3,padx=10)

        self.amount = tkinter.Entry()
        self.amount.grid(column=4,row=1)

        self.send_money_to_entry = tkinter.Entry()
        self.send_money_to_entry.grid(row=0,column=4,padx=10)

        self.send_button = tkinter.Button(width=33,bg="white",fg="black",text="send",command=self.send_money)
        self.send_button.grid(row=2,column=3,columnspan=2)

        self.new_pw = tkinter.Button(text="New Password",width=31,bg="white",fg="black",command=self.change_pw)
        self.new_pw.grid(row=3,column=3,columnspan=2)

        self.mainloop()


    def add_money(self):
        my_data = self.entry.get()
        with open("data.json", "r") as data:
            aa = json.load(data)
            aa[self.user]["money"]+=int(my_data)
        with open("data.json","w") as data:
            json.dump(aa,data,indent=4)
            self.entry.delete(0,"end")

    def get_moneyy(self):
        my_data = self.entry.get()
        with open("data.json", "r") as data:
            aa = json.load(data)
            aa[self.user]["money"] -= int(my_data)
        with open("data.json", "w") as data:
            json.dump(aa, data, indent=4)
            self.entry.delete(0, "end")

    def see_balance(self):
        with open("data.json","r") as data:
            d = json.load(data)
            my_data = d[self.user]["money"]
        self.balance_label.config(text=f"Your balance: {my_data}")
    def send_money(self):

        to = self.send_money_to_entry.get()
        amount = self.amount.get()
        question = messagebox.askquestion("", f"Are you sure you want to send {amount} to {to}?")
        if question!="no":
            print(question)
            try:
                with open("data.json", "r") as data:
                    aa = json.load(data)
                    if aa[self.user]["money"] >= int(amount):
                        aa[self.user]["money"]-=int(amount)

                        with open("data.json", "w") as data:
                            json.dump(aa, data, indent=4)
                            self.entry.delete(0, "end")
                            messagebox.showinfo(title="", message="Your transaction was completed without any problems!")

                        with open("data.json", "r") as data:
                            aa = json.load(data)
                            aa[to]["money"] += int(amount)
                        with open("data.json", "w") as data:
                            json.dump(aa, data, indent=4)
                            self.amount.delete(0, "end")
                            self.send_money_to_entry.delete(0,"end")
                    else:
                        m = messagebox.askquestion(message="You do not have enough money in your account would you like to borrow from the bank?",title="info")
                        if m!="no":
                            with open("data.json", "r") as data:
                                aa = json.load(data)
                                aa[self.user]["money"] -= int(amount)
                            with open("data.json", "w") as data:
                                json.dump(aa, data, indent=4)
                                self.entry.delete(0, "end")


                            with open("data.json", "r") as data:
                                aa = json.load(data)
                                aa[to]["money"] += int(amount)
                            with open("data.json", "w") as data:
                                json.dump(aa, data, indent=4)
                                self.amount.delete(0, "end")
                                self.send_money_to_entry.delete(0,"end")
                                messagebox.showinfo(title="",
                                                    message="Your transaction was completed without any problems!")
            except:
                pass
        else:
            pass
    def change_pw(self):
        self.destroy()
        new_pw_screen(self.user)



class Screen2(Tk):
    def __init__(self):
        super().__init__()
        self.config(bg="lightblue",pady=20)
        lab_user = tkinter.Label(text="Add user: ",fg="black",bg="white")
        lab_user.grid(row=0,column=0)
        pw_label = tkinter.Label(text="Add password: ",fg="black",bg="white")
        pw_label.grid(row=1,column=0)
        self.lab_entry = tkinter.Entry()
        self.lab_entry.grid(row=0,column=1)
        self.pw_entry=tkinter.Entry(show="_")
        self.pw_entry.grid(row=1,column=1,pady=20,padx=30)
        add_usser_pw = tkinter.Button(text="Add",width=32,command=lambda:self.add_user(self.pw_entry.get(),self.lab_entry.get()),bg="white",fg="black")
        add_usser_pw.grid(row=2,column=0,columnspan=2,pady=20,padx=30)
        self.mainloop()

    def add_user(self,p,u):
        user_pw = p
        user_name = u
        add = {user_name: {"password":user_pw, "money":0}}
        with open("data.json","r") as data:
            da = json.load(data)
            da.update(add)
        with open("data.json","w") as data:
            json.dump(da,data,indent=4)
            self.lab_entry.delete(0, "end")
            self.pw_entry.delete(0, "end")
            self.destroy()
