import game_framework


from pico2d import *

name = "LoseState"
image = None


def enter():
    global image
    image = load_image('etc/lose.png')


def exit():
    global image
    del(image)



def handle_events():
    global select_count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

def draw():
    global select_count
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
