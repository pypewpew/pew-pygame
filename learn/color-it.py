import pew

pew.init()
screen = pew.Pix()

pen_x, pen_y, pen_color = 0, 0, 0

while True:
    keys = pew.keys()
    if keys & pew.K_UP and pen_y > 0:
        pen_y = pen_y - 1
    elif keys & pew.K_LEFT and pen_x > 0:
        pen_x = pen_x - 1
    elif keys & pew.K_RIGHT and pen_x < 7:
        pen_x = pen_x + 1
    elif keys & pew.K_DOWN and pen_y < 7:
        pen_y = pen_y + 1
    
    if keys & pew.K_O:
        # french keyboard Z
        pen_color = pen_color + 1 if pen_color < 3 else 0
    
    if keys & pew.K_X:
        # french keyboard X
        screen.pixel(pen_x, pen_y, pen_color)

    pew.show(screen)
    pew.tick(1/12)