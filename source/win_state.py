import game_framework
import title_state

from pico2d import *

name = "WinState"
image = None


def enter():
    global image
    image = load_image('etc/win.png')


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
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
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
