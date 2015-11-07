import random
import json
import os

from pico2d import *

import game_framework
import title_state
import lose_state

name = "MainState"

Missile_List = []
Enemy_List = []
Enemy_Missile_List = []
Enemy_Explosion = []

background1 = None
player1 = None


class Timer:
    def __init__(self):
        self.time = 0
        self.timer = 0
        self.sec = 0
        self.min = 0

    def update(self):
        self.time += 0.02
        self.create_enemy()

    def create_enemy(self):
        if self.time >= 0.7:
            new_enemy = Enemy()
            Enemy_List.append(new_enemy)
            self.time = 0


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
        self.image = load_image('player/player1.png')
        self.frame = 6
        self.key_down = False
        self.left_move = 0
        self.right_move = 0

    def update(self):
        if self.left_move == 1:
            self.x = max(0, self.x - 5)
            self.frame -= 1
            if self.frame == 0 :
                self.frame = 6

        elif self.right_move == 1:
            self.x = min(800, self.x + 5)
            self.frame += 1
            if self.frame == 11 :
                self.frame = 6

    def draw(self):
        self.image.clip_draw(self.frame*64, 0, 64, 72, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -10, self.y + 10, self.x + 10, self.y - 36

    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)


class Missile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('missile/player_missile.png')

    def update(self) :
        global newmissile
        self.y += 8
        if(self.y > 600) :
            self.y = 0
            del Missile_List[0]

    def draw(self):
            self.image.draw(self.x, self.y + 30)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32, self.y + 28, self.x + 32, self.y - 48


class Enemy:
    def __init__(self):
        self.x, self.y = random.randint(50, 750), 550
        self.missile_count = 0
        self.image = load_image('enemy/enemy_4.png')

    def update(self):
        self.y -= 0.5
        if(self.y < 0):
            self.y = 550
            del Enemy_List[0]
        self.missile_count += 0.02
        if self.missile_count > 1 :
            self.missile_count = 0
            enemy_missile = Enemy_Missile(self.x, self.y)
            Enemy_Missile_List.append(enemy_missile)

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 37, self.y + 38, self.x + 37, self.y - 38


class Enemy_Missile:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('missile/enemy_missile.png')

    def update(self):
        self.y -= 8
        self.frame = (self.frame +1) % 2
        if self.y < 0:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 8, self.y + 8, self.x + 8, self.y - 8


class Explosion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.image = load_image('bomb/effect_death.png')

    def update(self):
        self.frame = (self.frame + 1) % 15
        if self.frame == 14:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)



def enter():
    global timer, background1, player1, Missile_List, Enemy_List, Enemy_Explosion, Enemy_Missile_List
    timer = Timer()
    background1 = BackGround()
    player1 = Player()
    Missile_List = []
    Enemy_List = []
    Enemy_Missile_List = []
    Enemy_Explosion = []

def exit():
    global timer, background1, player1
    del(timer)
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
            player1.frame = 5
            if event.key == SDLK_LEFT:
                player1.key_down = False
            elif event.key == SDLK_RIGHT:
                player1.key_down = False

def collision(a, b):
    a_left, a_bottom, a_right, a_top = a.get_bb()
    b_left, b_bottom, b_right, b_top = b.get_bb()

    if a_left > b_right :
        return False
    if a_right < b_left :
        return False
    if a_bottom < b_top :
        return False
    if a_top > b_bottom :
        return False
    return True


def update():
    global player1
    timer.update()
    background1.update()
    if player1.key_down == True:
        player1.update()

    for member in Missile_List:
        member.update()

    for member in Enemy_List:
        member.update()

    for member in Enemy_Missile_List:
        check_frame = member.update()
        if check_frame == False:
            Enemy_Missile_List.remove(member)

    for member in Enemy_Explosion:
        check_frame = member.update()
        if check_frame == False:
            Enemy_Explosion.remove(member)

    #플레이어 미사일과 적 기체가 충돌한다면
    for player_missile in Missile_List:
        for enemy_plane in Enemy_List:
            if collision(player_missile, enemy_plane):
                Missile_List.remove(player_missile)
                Enemy_List.remove(enemy_plane)
                enemy_explosion = Explosion(enemy_plane.x, enemy_plane.y)
                Enemy_Explosion.append(enemy_explosion)

    #적 기체의 미사일과 플레이어가 충돌한다면
    for enemy_plane_missile in Enemy_Missile_List:
        if collision(enemy_plane_missile, player1):
            game_framework.push_state(lose_state)





def draw():
    handle_events()
    clear_canvas()
    background1.draw()
    player1.draw()

    for member in Missile_List:
        member.draw()

    for member in Enemy_List:
        member.draw()

    for member in Enemy_Missile_List:
        member.draw()

    for member in Enemy_Explosion:
        member.draw()

    update_canvas()




