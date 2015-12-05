import game_framework
import title_state

from pico2d import *

name = "LoseState"
image = None
bgm = None


def enter():
    global image, bgm
    image = load_image('etc/lose.png')
    bgm = load_music('music/lose.ogg')
    bgm.set_volume(64)
    bgm.play(1)


def exit():
    global image
    del(image)


def handle_events(frame_time):
    global select_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title_state)

def draw(frame_time):
    global select_count
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass
