from turtle import Turtle

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color('white')
        self.penup()
        self.score = 0
        self.write(f"Score: {self.score}")
    def add_score(self):
        self.clear()
        self.score+=1
        self.write(f"Score: {self.score}")
