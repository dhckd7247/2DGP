import random
import json
import os

from pico2d import *

import game_framework
import title_state

name = "MainState"

Missile_List = []

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
    #LEFT_OVER, LEFT, STAND, RIGHT, RIGHT_OVER = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y = 400, 50
        self.image = load_image('player/player1_.png')
        self.frame = 6
        self.key_down = False
        self.left_move = 0
        self.right_move = 0

    def update(self):
        if self.left_move == 1:
            self.x -= 5
            self.frame -= 1
            if self.frame == 0 :
                self.frame = 6


        elif self.right_move == 1:
            self.x += 5
            self.frame += 1
            if self.frame == 11 :
                self.frame = 6



    def draw(self):
        self.image.clip_draw(self.frame*64, 0, 64, 72, self.x, self.y)

    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)


class Missile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('missile/player_missile.png')

    def update(self) :
        self.y += 5
        if(self.y > 600) :
            self.y = 0
            del Missile_List[0]

    def draw(self):
            self.image.draw(self.x, self.y + 30)


def enter():
    global background1, player1, Missile_List
    background1 = BackGround()
    player1 = Player()
    Missile_List = []

def exit():
    global background1, player1
    del(background1)
    del(player1)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

            elif event.key == SDLK_LEFT:
                player1.key_down = True
                player1.left_move = 1
                player1.right_move = 0

            elif event.key == SDLK_RIGHT:
                player1.key_down = True
                player1.right_move = 1
                player1.left_move = 0

            elif event.key == SDLK_SPACE:
                player1.missile_shoot()

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                player1.key_down = False
            elif event.key == SDLK_RIGHT:
                player1.key_down = False


def update():
    background1.update()
    if player1.key_down == True:
        player1.update()

    for member in Missile_List:
        member.update()


def draw():
    handle_events()
    clear_canvas()
    background1.draw()
    player1.draw()

    for member in Missile_List:
        member.draw()

    update_canvas()




