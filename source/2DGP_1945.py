from pico2d import*
open_canvas()
map_sky = load_image('background/background_sky.png')
map_space = load_image('background/background_space.png')

def handle_events():
    global play
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            play = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                play = False
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



class Player:
    def __init__(self):
        self.x, self.y = 400, 50
        self.image = load_image('player/player1_.png')
        self.frame = 6

    def draw(self):
        self.image.clip_draw(self.frame*64, 0, 64, 72, self.x, self.y)



sky_y = 300
sky_y2 = 900

play = True
player1 = Player()

while(sky_y > -300 and play):
    handle_events()

    clear_canvas()
    map_sky.clip_draw(0, 0, 800, 600, 400, sky_y2 )
    map_sky.clip_draw(0, 0, 800, 600, 400, sky_y)
    player1.draw()
    update_canvas()
    sky_y -= 1
    sky_y2 -= 1
    if (sky_y == -299):
        sky_y = 300
        sky_y2 = 900
    delay(0.01)

close_canvas()



