import game_framework
import select_state
import os
from pico2d import *

name = "TitleState"
image = None
bgm = None

def enter():
    global image, bgm
    open_canvas()
    image = load_image('etc/main.png')
    bgm = load_music('music/main.ogg')
    bgm.set_volume(64)
    bgm.repeat_play()

def exit():
    global image, bgm
    del(image)
    close_canvas()
    bgm.stop()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(select_state)


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass