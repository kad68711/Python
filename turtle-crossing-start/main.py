import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
player = Player()
car = CarManager()
score=Scoreboard()



screen.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_right, "Right")
screen.onkeypress(player.move_left, "Left")
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()
    car.create_car()
    car.move_car()

    for cars in car.all_cars:
        if cars.distance(player) < 20:
            game_is_on = False
            score.game_over()

    if player.is_at_finishline():
        player.go_to_start()
        car.levelup()
        score.increase_level()
           


screen.exitonclick()
