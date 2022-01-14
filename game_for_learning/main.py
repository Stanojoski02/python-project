# python-project
BACKGROUND_COLOR = "#B1DDC6"
import tkinter
import pandas
import random
import time

try:
    data = pandas.read_csv("data/words_to_learn")
    if len(data) < 20:
        data = pandas.read_csv("data/french_words.csv")
except:
    data = pandas.read_csv("data/french_words.csv")


to_learn = data.to_dict(orient="records")
choice = {}

def wr():

    global choice
    to_learn.remove(choice)
    choice = random.choice(to_learn)
    word = choice["French"]
    canvas.itemconfig(word_text, text=word, fill="black")
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(img, image=front_img)
    screen.after(3000, func=flip)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn")

def next_card():
    global choice
    choice = random.choice(to_learn)
    word = choice["French"]
    canvas.itemconfig(word_text,text=word,fill="black")
    canvas.itemconfig(title_text,text="French",fill="black")
    canvas.itemconfig(img,image=front_img)
    screen.after(3000, func=flip)



def flip():
    canvas.itemconfig(img, image=back_img)
    canvas.itemconfig(title_text, text="English",fill="white")
    canvas.itemconfig(word_text, text=choice["English"],fill="white")


screen = tkinter.Tk()
screen.title("Flashy")
screen.config(bg=BACKGROUND_COLOR,pady=50,padx=50)

front_img = tkinter.PhotoImage(file="images/card_front.png")
right_image = tkinter.PhotoImage(file="images/right.png")
wrong_image = tkinter.PhotoImage(file="images/wrong.png")
back_img = tkinter.PhotoImage(file="images/card_back.png")

canvas = tkinter.Canvas(width=800,height=526)
img = canvas.create_image(400,263,image=front_img)
title_text=canvas.create_text(400,150,text="title",font=("Ariel",40,"italic"))
word_text = canvas.create_text(400,263,text="Word",font=("ariel",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(column=0,row=0,columnspan=2)

true_button = tkinter.Button(image = right_image,command=wr)
true_button.grid(row=2,column=1)
wrong_button = tkinter.Button(image = wrong_image,command=next_card())
wrong_button.grid(row=2,column=0)


next_card()
screen.after(3000, func=flip)



screen.mainloop()


