import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

background1 = None
player1 = None


class BackGround:
    def __init__(self):
        self.y1, self.y2 = 300, 900
        self.image1 = load_image('background/background_sky.png')
        self.image2 = load_image('background/background_space.png')

    def update(self):
        self.y1 -= 1
        self.y2 -= 1
        if(self.y1 == -299):
            self.y1 = 300
            self.y2 = 900
        delay(0.01)

    def draw(self):
        self.image1.clip_draw(0, 0, 800, 600, 400, self.y2)
        self.image1.clip_draw(0, 0, 800, 600, 400, self.y1)


class Player:
    def __init__(self):
        self.x, self.y = 400, 50
        self.image = load_image('player/player1_.png')
        self.frame = 6
        self.missile = [load_image('missile/player_missile.png'), load_image('missile/player_missile2.png'),
                       load_image('missile/player_missile3.png'), load_image('missile/player_missile4.png')]
        self.missile_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.missile_y = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
        self.shoot_count = 0



    def draw(self):
        self.image.clip_draw(self.frame*64, 0, 64, 72, self.x, self.y)

    def shoot_update(self):
        if(self.shoot_count == 1) :
            self.missile_y[0] += 5

    def shoot(self):
        for i in range(0, 10) :
            self.missile[0].clip_draw(0, 0, 64, 96, self.missile_x[0], self.y + self.missile_y[0])


def enter():
    global background1, player1
    background1 = BackGround()
    player1 = Player()


def exit():
    global background1, player1
    del(background1)
    del(player1)


def pause():
    pass


def resume():
    pass


def handle_events():
    global player1
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

            elif event.key == SDLK_LEFT:
                player1.x -= 10
                player1.frame -= 1
                if player1.frame == 0 :
                    player1.frame = 6

            elif event.key == SDLK_RIGHT:
                player1.x += 10
                player1.frame += 1
                if player1.frame == 11 :
                    player1.frame = 6

            elif event.key == SDLK_SPACE:
                player1.missile_x[0] = player1.x
                player1.shoot_count = 1



def update():
    background1.update()
    player1.shoot_update()


def draw():
    handle_events()
    clear_canvas()
    background1.draw()
    player1.draw()
    if player1.shoot_count == 1 :
        player1.shoot()
    update_canvas()




