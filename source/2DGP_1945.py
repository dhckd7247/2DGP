from pico2d import*
open_canvas()
map_sky = load_image('background/background_sky.png')
map_space = load_image('background/background_space.png')

y = 300
y2 = 900
while(y > -300):
    clear_canvas()
    map_sky.clip_draw(0, 0, 800, 600, 400, y2 )
    map_sky.clip_draw(0, 0, 800, 600, 400, y)
    update_canvas()
    y -= 1
    y2 -= 1
    if (y == -299):
        y = 300
        y2 = 900

    delay(0.01)

close_canvas()



