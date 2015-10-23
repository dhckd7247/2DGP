import game_framework
import main_state
from pico2d import *

name = "SelectState"
image1 = None
image2 = None
select = None
select_count = None


def enter():
    global image1, image2, select, select_count
    select_count = 1
    image1 = load_image('etc/select_player1.png')
    image2 = load_image('etc/select_player2.png')
    select = load_image('etc/select.png')


def exit():
    global image1, image2, select, select_count
    del(image1)
    del(image2)
    del(select)
    del(select_count)


def handle_events():
    global select_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.push_state(main_state)
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                select_count = 3
            elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                select_count = 1

def draw():
    global select_count
    clear_canvas()
    image1.draw(200, 300)
    image2.draw(600, 300)
    select.draw(200 * select_count, 300)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
