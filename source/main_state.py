import random
import json
import os

from pico2d import *

import game_framework
import title_state
import lose_state

name = "MainState"

Missile_List = []
Special_Missile_List = []
Enemy_List = []
Enemy_Missile_List = []
Enemy_Explosion = []
Middle_Boss_List = []
Item_List = []

background1 = None
player1 = None
special_count = None


class Timer:
    def __init__(self):
        self.enemy_time = 0
        self.middleboss_time = 0
        self.sec = 0
        self.min = 0

    def update(self, frame_time):
        self.enemy_time += frame_time
        self.middleboss_time += frame_time
        self.create_enemy()
        self.create_middle_boss()

    def create_enemy(self):
        if self.enemy_time >= 0.7:
            new_enemy = Enemy()
            Enemy_List.append(new_enemy)
            self.enemy_time = 0

    def create_middle_boss(self):
        if self.middleboss_time >= 10.0:
            new_middle_boss = Middle_Boss()
            Middle_Boss_List.append(new_middle_boss)
            self.middleboss_time = 0


class BackGround:
    MOVE_PER_SEC = 50

    def __init__(self):
        self.y1, self.y2 = 300, 900
        self.image1 = load_image('background/background_sky.png')
        self.image2 = load_image('background/background_space.png')

    def update(self, frame_time):
        speed = frame_time * self.MOVE_PER_SEC
        self.y1 -= speed
        self.y2 -= speed
        if self.y1 <= -299 :
            self.y1 = 300
            self.y2 = 900

    def draw(self):
        self.image1.clip_draw(0, 0, 800, 600, 400, self.y2)
        self.image1.clip_draw(0, 0, 800, 600, 400, self.y1)


class Player:
    MOVE_PER_SEC = 400

    def __init__(self):
        self.x, self.y = 400, 50
        self.image = load_image('player/player1.png')
        self.frame = 6
        self.key_down = False
        self.left_move = 0
        self.right_move = 0
        self.special_count = 1

    def update(self, frame_time):
        move_distance = frame_time * self.MOVE_PER_SEC
        if self.left_move == 1:
            self.x = max(0, self.x - move_distance)
            self.frame -= 1
            if self.frame == 1 :
                self.frame = 6

        elif self.right_move == 1:
            self.x = min(800, self.x + move_distance)
            self.frame += 1
            if self.frame == 11 :
                self.frame = 6

    def draw(self):
        self.image.clip_draw(self.frame*64, 0, 64, 72, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x -10, self.y + 25, self.x + 10, self.y - 36

    def missile_shoot(self):
        newmissile = Missile(self.x, self.y)
        Missile_List.append(newmissile)

    def special_missile_shoot(self):
        if player1.special_count > 0 :
            newspecialmissile = Special_Missile()
            newspecialmissile.num = self.special_count
            Special_Missile_List.append(newspecialmissile)
            self.special_count -= 1


class Missile:
    MOVE_PER_SEC = 600

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('missile/player_missile.png')

    def update(self, frame_time) :
        move_distance = frame_time * self.MOVE_PER_SEC
        global newmissile
        self.y += move_distance
        if self.y > 600 :
            self.y = 0
            del Missile_List[0]

    def draw(self):
        self.image.draw(self.x, self.y + 30)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32, self.y + 30, self.x + 32, self.y - 18


class Special_Missile:
    MOVE_PER_SEC = 300
    FRAME_PER_SEC = 5

    def __init__(self):
        self.x, self.y = 1, 0
        self.i = 100
        self.num = 1
        self.count = 30
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('item/item_missile.png')

    def update(self, frame_time):
        move_distance = frame_time * self.MOVE_PER_SEC
        self.total_frames += frame_time * self.FRAME_PER_SEC
        global newspecialmissile
        self.y += move_distance
        self.frame = int(self.total_frames) % 17
        if self.y > 600 :
            self.y = 0
            del Special_Missile_List[0]
        if self.frame == 16:
            self.frame = 16

    def draw(self):
        for i in range(17) :
            self.image.clip_draw(self.frame * 31, 0, 30, 128, 50 * i, self.y )

    def draw_count(self):
        global player1
        if player1.special_count == 1:
            self.image.clip_draw(0, 0, 31, 128, 700, 0)
        elif player1.special_count == 2:
            self.image.clip_draw(0, 0, 31, 128, 700, 0)
            self.image.clip_draw(0, 0, 31, 128, 730, 0)
        elif player1.special_count == 3:
            self.image.clip_draw(0, 0, 31, 128, 700, 0)
            self.image.clip_draw(0, 0, 31, 128, 730, 0)
            self.image.clip_draw(0, 0, 31, 128, 760, 0)


class Enemy:
    MOVE_PER_SEC = 30
    SHOT_PER_SEC = 1

    def __init__(self):
        self.x, self.y = random.randint(50, 750), 550
        self.missile_count = 0
        self.image = load_image('enemy/enemy_4.png')

    def update(self, frame_time):
        speed = frame_time * self.MOVE_PER_SEC
        self.y -= speed
        if(self.y < 0):
            self.y = 550
            del Enemy_List[0]
        self.missile_count += frame_time * self.SHOT_PER_SEC
        if self.missile_count > 0.8 :
            self.missile_count = 0
            enemy_missile = Enemy_Missile(self.x, self.y - 30)
            Enemy_Missile_List.append(enemy_missile)

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 37, self.y + 38, self.x + 37, self.y - 38


class Middle_Boss:
    MOVE_PER_SEC = 20
    SHOT_PER_SEC = 0.5

    def __init__(self):
        self.x, self.y = random.randint(200, 500), 500
        self.i = -40
        self.image = load_image('boss/middleboss_1.png')
        self.hp = 10
        self.missile_count = 0

    def update(self, frame_time):
        speed = frame_time * self.MOVE_PER_SEC
        self.y -= speed

        self.missile_count += frame_time * self.SHOT_PER_SEC
        if self.missile_count > 0.7 :
            self.missile_count = 0
            for i in range(5) :
                enemy_missile = Enemy_Missile(self.x + self.i, self.y - 30)
                Enemy_Missile_List.append(enemy_missile)
                self.i += 20
            self.i = -40

    def draw(self):
        self.image.draw(self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 115, self.y + 80, self.x + 115, self.y - 50


class Enemy_Missile:
    MOVE_PER_SEC = 600
    FRAME_PER_SEC = 5

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('missile/enemy_missile.png')

    def update(self, frame_time):
        speed = frame_time * self.MOVE_PER_SEC
        self.total_frames += frame_time * self.FRAME_PER_SEC
        self.y -= speed
        self.frame = int(self.total_frames) % 3
        if self.y < 0:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 8, self.y + 8, self.x + 8, self.y - 3


class Explosion:
    FRAME_PER_SEC = 50

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('bomb/effect_death.png')

    def update(self, frame_time):
        self.total_frames += frame_time * self.FRAME_PER_SEC
        self.frame = int(self.total_frames) % 15
        if self.frame == 14:
            return False

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)


class Item:
    FRAME_PER_SEC = 5
    FRAME_PER_MOVE = 100

    def __init__(self,x, y):
        self.x, self.y = x, y
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('item/item.png')

    def update(self, frame_time):
        speed = frame_time * self.FRAME_PER_MOVE
        self.total_frames += frame_time * self.FRAME_PER_SEC
        self.frame = int(self.total_frames) % 3
        self.y -= speed
        if self.y < 0:
            del Item_List[0]

    def draw(self):
        self.image.clip_draw(self.frame * 54, 0, 54, 32, self.x, self.y)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 27, self.y + 16, self.x + 27, self.y - 16


def enter():
    global timer, background1, player1, special_count, Missile_List, Special_Missile_List, Enemy_List, Enemy_Explosion, Enemy_Missile_List, Middle_Boss_List, Item_List
    timer = Timer()
    background1 = BackGround()
    player1 = Player()
    special_count = Special_Missile()
    Missile_List = []
    Special_Missile_List = []
    Enemy_List = []
    Enemy_Missile_List = []
    Enemy_Explosion = []
    Middle_Boss_List = []
    Item_List = []


def exit():
    global timer, background1, player1, special_count
    del(timer)
    del(background1)
    del(player1)
    del(special_count)


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
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

            elif event.key == SDLK_z:
                player1.special_missile_shoot()

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


def update(frame_time):
    global player1
    timer.update(frame_time)
    background1.update(frame_time)
    if player1.key_down == True:
        player1.update(frame_time)

    for member in Missile_List:
        member.update(frame_time)

    for member in Special_Missile_List:
        member.update(frame_time)
        for enemy_plane in Enemy_List:
            Enemy_List.remove(enemy_plane)
            enemy_explosion = Explosion(enemy_plane.x, enemy_plane.y)
            Enemy_Explosion.append(enemy_explosion)
            for enemy_plane_missile in Enemy_Missile_List:
                Enemy_Missile_List.remove(enemy_plane_missile)

    for member in Enemy_List:
        member.update(frame_time)

    for member in Enemy_Missile_List:
        check_frame = member.update(frame_time)
        if check_frame == False:
            Enemy_Missile_List.remove(member)

    for member in Enemy_Explosion:
        check_frame = member.update(frame_time)
        if check_frame == False:
            Enemy_Explosion.remove(member)

    for member in Middle_Boss_List:
        member.update(frame_time)

    for member in Item_List:
        member.update(frame_time)

    #플레이어 미사일과 적 기체가 충돌한다면
    for player_missile in Missile_List:
        for enemy_plane in Enemy_List:
            if collision(player_missile, enemy_plane):
                Missile_List.remove(player_missile)
                Enemy_List.remove(enemy_plane)
                enemy_explosion = Explosion(enemy_plane.x, enemy_plane.y)
                Enemy_Explosion.append(enemy_explosion)

    #플레이어 미사일과 적 중간보스가 충돌한다면
    for player_missile in Missile_List:
        for middle_boss in Middle_Boss_List:
            if collision(player_missile, middle_boss):
                Missile_List.remove(player_missile)
                middleboss_explosion = Explosion(player_missile.x, player_missile.y)
                Enemy_Explosion.append(middleboss_explosion)
                middle_boss.hp -= 1
                if middle_boss.hp == 0:
                    Middle_Boss_List.remove(middle_boss)
                    item = Item(middle_boss.x, middle_boss.y)
                    Item_List.append(item)


    #적 기체의 미사일과 플레이어가 충돌한다면
    for enemy_plane_missile in Enemy_Missile_List:
        if collision(enemy_plane_missile, player1):
            game_framework.push_state(lose_state)

    #아이템과 플레이어가 충돌한다면
    for item in Item_List:
        if collision(item, player1):
            Item_List.remove(item)
            player1.special_count += 1


def draw(frame_time):
    clear_canvas()
    background1.draw()
    player1.draw()
    if player1.special_count > 0 :
        special_count.draw_count()
    #player1.draw_bb()

    for member in Missile_List:
        member.draw()
        #member.draw_bb()

    for member in Special_Missile_List:
        member.draw()

    for member in Enemy_List:
        member.draw()
        #member.draw_bb()

    for member in Enemy_Missile_List:
        member.draw()
        #member.draw_bb()

    for member in Enemy_Explosion:
        member.draw()

    for member in Middle_Boss_List:
        member.draw()

    for member in Item_List:
        member.draw()

    update_canvas()




