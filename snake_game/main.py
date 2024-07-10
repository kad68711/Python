from turtle import Screen
from snake import Snake
import time
from food import FOOD
from scoreboard import SCOREBOARD

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = FOOD()
score = SCOREBOARD()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.5)

    snake.move()
    if snake.head.distance(food) < 15:
        score.increase_score()
        food.refresh()
        snake.extend()
    if snake.head.xcor()>280 or snake.head.xcor()<-280 or snake.head.ycor()>280 or snake.head.ycor()<-280:
        game_is_on=False
        score.update_scoreboard()
    for segment in snake.segment[1:]:
        if snake.head.distance(segment)<10:
            game_is_on=False
            score.reset()



screen.exitonclick()
