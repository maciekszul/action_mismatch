# exp dev

from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import numpy as np


# monitor settings
x230 = (56, 56, (1366, 768))

width, dist, res = x230

mon = monitors.Monitor("default")
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)

win = visual.Window(
    size=res,
    color="#A9A9A9",
    fullscr=True,
    allowGUI=False,
    winType="pyglet",
    units="deg",
    monitor=mon
)

# stim
outer = visual.Circle(
    win,
    10, 
    edges=100
)

inner = visual.Circle(
    win, 
    1, 
    edges=100, 
    fillColor="#A9A9A9", 
    lineColor="#A9A9A9"
)

bar_h = 2
bar_w = 0.2
bar_shape = [
    [-(bar_w/2), -(bar_h/2)],
    [-(bar_w/2), (bar_h/2)],
    [(bar_w/2), (bar_h/2)],
    [(bar_w/2), -(bar_h/2)]
]

tbar_h = 2
tbar_w = 0.2
tbar_shape = bar_shape

timebar_background = visual.ShapeStim(
    win,
    vertices=bar_shape,
    units="deg",
    closeShape=True,
    fillColor="white"
)

timebar_foreground = visual.ShapeStim(
    win,
    vertices=tbar_shape,
    units="deg",
    closeShape=True,
    fillColor="red",
)



wedge1 = visual.RadialStim(
    win, 
    color="gray", 
    size=20,
    visibleWedge=[0, 45], 
    radialCycles=0, 
    angularCycles=1, 
    interpolate=False,
    autoLog=False,
    units="deg"
    )
# wedge2 = visual.RadialStim(
#     win, 
#     tex='sqrXsqr', 
#     color=-1, 
#     size=15,
#     visibleWedge=[0, 45], 
#     radialCycles=6, 
#     angularCycles=8, 
#     interpolate=False,
#     autoLog=False,
#     units="deg"
#     )


# exp
timer_dur = 1.2
timer = core.CountdownTimer(timer_dur)

while timer.getTime() > 0:
    wedge1.ori += 15
    wedge1.draw()
    inner.draw()
    timebar_background.draw()
    time_prop = 1 - (timer.getTime() / timer_dur)
    tbar_shape = [
        [-(tbar_w/2), -(tbar_h/2)],
        [-(tbar_w/2), -(tbar_h/2) + time_prop * bar_h],
        [(tbar_w/2), -(tbar_h/2) + time_prop * bar_h],
        [(tbar_w/2), -(tbar_h/2)]
    ]
    timebar_foreground.vertices = tbar_shape
    timebar_foreground.draw()
    outer.draw()
    win.flip()


win.close()
core.quit()