import game_framework
import main_state
from pico2d import *

name = "SelectState"
image1 = None
image2 = None


def enter():
    global image1, image2
    image1 = load_image('etc/select_player1.png')
    image2 = load_image('etc/select_player2.png')


def exit():
    global image1, image2
    del(image1)
    del(image2)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(main_state)


def draw():
    clear_canvas()
    image1.draw(200, 300)
    image2.draw(600, 300)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
