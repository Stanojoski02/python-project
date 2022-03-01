import turtle
import time
from snake import Snake
from food import Food
from score import Score

screen = turtle.Screen()
screen.setup(width=600,height=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)



snake = Snake()
food = Food()
score = Score()

screen.listen()

screen.onkey(snake.left,'Left')
screen.onkey(snake.right,'Right')

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.3)
    snake.move()

    if snake.head.distance(food)<20:
        food.change_location()
        snake.extend()
        score.add_score()

    if snake.head.xcor() > 300 or snake.head.xcor() < -300 or snake.head.ycor() > 300 or snake.head.ycor()< -300:
        game_is_on = False



screen.exitonclick()
