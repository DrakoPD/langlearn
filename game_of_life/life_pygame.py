import pygame as pg
import math

pg.init()

inactive_color = (0,0,0)
active_color = (255,255,255)
cursor_color = (62, 222, 137)

rs = 50

cells = {}
run = False

gameDisplay = pg.display.set_mode((800,600))
gameDisplay.fill((0,0,0))

update = pg.USEREVENT + 1

while True:
    x,y = pg.mouse.get_pos()
    _,x = math.modf(x/rs)
    _,y = math.modf(y/rs)



    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                pass
            if event.key == pg.K_SPACE:
                run = not run
                pg.time.set_timer(update, 500*run)

        if event.type == pg.MOUSEBUTTONDOWN and not run:
            if (x,y) in cells:
                del cells[(x,y)]
            else:
                cells[(x,y)] = [(x*rs,y*rs,rs,rs),(x,y),0,1]
        if event.type == update:
            mitosis = cells.copy()
            for key,value in mitosis.items():
                for i in range(0,3):
                    for f in range(0,3):
                        xc = value[1][0] + i -1
                        yc = value[1][1] + f -1
                        if not ((i - 1) == 0 and (f - 1)==0): 
                            if (xc,yc) in cells:
                                cells[(xc,yc)][2] += 1
                            else:
                                cells[(xc,yc)] = [(xc*rs,yc*rs,rs,rs),(xc,yc),1,0]
            
            mitosis = cells.copy()
            for key, value in mitosis.items():
                if value[2] < 2 or value[2] > 3:
                    del cells[key]
                elif value[2] == 2 and value[3] == 0:
                    del cells[key]
                elif value[2] == 3 and value[3] == 0:
                    cells[key][3] = 1
                    cells[key][2] = 0
                else:
                    cells[key][2] = 0    

    gameDisplay.fill((inactive_color))
    for key,cell in cells.items():
        pg.draw.rect(gameDisplay,active_color,cell[0])
    if not run:
        pg.draw.rect(gameDisplay, cursor_color,(rs*x,rs*y,rs,rs),10)

    pg.display.flip()