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

wedge_rad = [0, 25]
wedge_size = 20

wedge0 = visual.RadialStim(
    win, 
    color="gray", 
    size=wedge_size,
    visibleWedge=wedge_rad, 
    radialCycles=0, 
    angularCycles=1, 
    interpolate=False,
    autoLog=False,
    units="deg"
    )

wedge1 = visual.RadialStim(
    win, 
    tex="sqrXsqr",
    color=1, 
    size=wedge_size,
    visibleWedge=wedge_rad, 
    radialCycles=4, 
    angularCycles=8, 
    interpolate=False,
    autoLog=False
)
wedge2 = visual.RadialStim(
    win, 
    tex='sqrXsqr', 
    color=-1, 
    size=wedge_size,
    visibleWedge=wedge_rad, 
    radialCycles=4, 
    angularCycles=8, 
    interpolate=False,
    autoLog=False
)

global_clock = core.Clock()

# exp

flash_period = 0.1
timer_dur = 5
timer = core.CountdownTimer(timer_dur)
while timer.getTime() > 0:
    t = global_clock.getTime()
    if t % flash_period < flash_period / 2.0:  # more accurate to count frames
        stim = wedge1
    else:
        stim = wedge2
    stim.ori += 3
    stim.draw()
    # wedge0.ori += 3
    # wedge0.draw()
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