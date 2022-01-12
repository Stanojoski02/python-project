import turtle

import pandas

screen =  turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

pras = pandas.read_csv("50_states.csv")
lis = pras["state"].to_list()
print(pras)



game_on = []
while len(game_on) < 45:

    answer = screen.textinput(title="Ques the state", prompt="What another state name?").title()
    if answer == "exit":
        break
    if answer in lis:
        game_on.append(answer)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = pras[pras["state"] == answer]
        t.goto(int(state_data.x), int(state_data.y))
        b = pras[pras["state"] == answer]
        t.write(answer)
        print(b)
turtle.mainloop()

