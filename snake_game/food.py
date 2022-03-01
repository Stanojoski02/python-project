from turtle import Turtle
import random
COLORS = ['red','blue','yellow','white']

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color(COLORS[1])
        self.goto(random.randint(0,280),random.randint(0,280))
        self.shapesize(0.5,0.5)
    def change_location(self):
        self.color(random.choice(COLORS))
        self.goto(random.randint(0, 280), random.randint(0, 280))
