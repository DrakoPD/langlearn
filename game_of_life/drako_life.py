"""
Juego de la vid_, reglas:

- Si una celda está ENCENDIDA y tiene menos de dos vecinos que están ENCENDIDOS, se APAGA
- Si una celda está ENCENDIDA y tiene dos o tres vecinos que están ENCENDIDOS, permanece ENCENDIDA.
- Si una celda está ENCENDIDA y tiene más de tres vecinos que están ENCENDIDOS, se APAGA.
- Si una celda está apagada y tiene exactamente tres vecinos que están encendidos, se enciende.
"""

import time
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

# ---------- Variables globales -----------
fig = plt.figure(figsize=(7, 9))
ax = fig.add_subplot(111)
plt.subplots_adjust(bottom = 0.2)

ax.set_xlim([-25, 25])
ax.set_ylim([-25, 25])

run = False
cells = {}
move = None
point = None
timer = fig.canvas.new_timer(interval=500)

event_click = None
event_enter = None
event_leave = None
btnstart = None

# ---------- Clic Nueva Celula ----------
def onclick(event):
    _, xi = math.modf(event.xdata)
    _, yi = math.modf(event.ydata)
    nuevo = True

    if (xi,yi) in cells:
        nuevo = False
        cells[(xi,yi)][1].remove()
        del cells[(xi,yi)]

    if nuevo:
        p, = ax.plot(xi, yi, 'sr')
        cells[(xi,yi)] = [[xi,yi], p,1,0]

prex = 0
prey = 0
def motion(event):
    global point
    global prex
    global prey

    _, xi = math.modf(event.xdata)
    _, yi = math.modf(event.ydata)
    if (xi != prex or yi != prey):
        point.set_data(xi,yi)
        plt.show()
        prex = xi
        prey = yi

def enter(event):
    global move
    global point
    point, = ax.plot(0, 0, 'sb')
    move = fig.canvas.mpl_connect('motion_notify_event',motion)

def leave(event):
    global move
    global point
    fig.canvas.mpl_disconnect(move)
    point.remove()
    plt.show()

# ---------- Botones ----------
class Index(object):
    ind = 0
    global run
    global timer
    global btnstart
    global point

    global event_click
    global event_enter
    global event_leave
    global move

    def start(self, event):
        point.remove()

        fig.canvas.mpl_disconnect(move)
        fig.canvas.mpl_disconnect(event_click)
        fig.canvas.mpl_disconnect(event_enter)
        fig.canvas.mpl_disconnect(event_leave)

        run = True
        timer.start    
        btnstart.on_clicked(callback.stop)
        btnstart.label("Stop")

        plt.show()

    def stop(self, event):
        event_click = fig.canvas.mpl_connect('button_press_event', onclick)
        event_enter = fig.canvas.mpl_connect('axes_enter_event',enter)
        event_leave = fig.canvas.mpl_connect('axes_leave_event',leave)

        run = False
        timer.cancel()
        btnstart.on_clicked(callback.start)
        btnstart.label("Start")

        plt.show()

# ---------- Iniciar Ciclo ----------


def ciclo():
    mitosis = cells.copy()

    for key, cell in mitosis.items():
        for i in range(0,3):
            for f in range(0,3):
                x = cell[0][0] - 1 + i
                y = cell[0][1] - 1 + f

                if (x,y) in cells:
                    cells[key][3] += 1
                else:
                    cells[(x,y)] = [[x,y],None,0,1]
    
    mitosis = cells.copy()

    for key, cell in mitosis.items():
        if cell[2]:
            if cell[3] < 2:
                cells[key][1].remove()
                del cells[key]
            if cell[3] > 3:
                cells[key][1].remove()
                del cells[key]
        else:
            if cell[3] == 3:
                x = cell[0][0]
                y = cell[0][1]

                p, = ax.plot(x, y, 'sr')
                cells[key][1] = p
            else:
                del cells[key]
    
    plt.show()
        



timer.add_callback(ciclo, ax)
# ---------- Iniciar Board ----------


event_click = fig.canvas.mpl_connect('button_press_event', onclick)
event_enter = fig.canvas.mpl_connect('axes_enter_event',enter)
event_leave = fig.canvas.mpl_connect('axes_leave_event',leave)

#axbtn = plt.axes([0.5, 0.01, 0.1, 0.075])
callback = Index()
#btnstart = Button(axbtn,'Start')
#btnstart.on_clicked(callback.start)


plt.show()