from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from psychopy import clock
from psychopy.hardware import joystick
import psychopy.tools.coordinatetools as ct
import os.path as op
import numpy as np
import pandas as pd
import misc


# exp settings
background_color = "#c7c7c7"
# exp_gray = "#c2c2c2"
exp_gray = "#b8b8b8"

wedge_rad = [0, 360]
wedge_size = 15

obs_time = 1

flickering_freq = 8

rotation_total_angle = 360

# time bar background shape
bar_h = 1.7
bar_w = bar_h/4
bar_shape = [
    [-(bar_w/2), -(bar_h/2)],
    [-(bar_w/2), (bar_h/2)],
    [(bar_w/2), (bar_h/2)],
    [(bar_w/2), -(bar_h/2)]
]

ut = 1





# monitor settings
x230 = (28, 56, (1366, 768))
lab = (53, 65, (1920, 1080))

width, dist, res = lab

mon = monitors.Monitor("default")
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)

win = visual.Window(
    size=res,
    color=background_color,
    fullscr=True,
    allowGUI=False,
    winType="pyglet",
    units="deg",
    monitor=mon
)

framerate = win.getActualFrameRate(
    nIdentical=10,
    nMaxFrames=60,
    nWarmUpFrames=10,
    threshold=1
)

framerate_r = np.round(framerate)
frame_spacing = int(np.round(framerate_r / flickering_freq))

# stim
inner = visual.Circle(
    win, 
    1, 
    edges=100, 
    fillColor=background_color, 
    lineColor=background_color
)

outer = visual.Circle(
    win, 
    wedge_size/2, 
    edges=100, 
    fillColor=exp_gray, 
    lineColor=background_color
)

timebar_background = visual.ShapeStim(
    win,
    vertices=bar_shape,
    units="deg",
    closeShape=True,
    fillColor="white"
)

try:
    wedge_cover = visual.RadialStim(
        win,
        tex="sqr",
        contrast=-1,
        color=background_color,
        size=wedge_size,
        visibleWedge=[0, 90], 
        radialCycles=1, 
        angularCycles=1, 
        interpolate=False,
        autoLog=False
    )

    wedge1 = visual.RadialStim(
        win, 
        tex="sqrXsqr",
        color=1, 
        size=wedge_size,
        visibleWedge=wedge_rad, 
        radialCycles=8, 
        angularCycles=30, 
        interpolate=False,
        autoLog=False
    )

    wedge2 = visual.RadialStim(
        win, 
        tex="sqrXsqr", 
        color=-1, 
        size=wedge_size,
        visibleWedge=wedge_rad, 
        radialCycles=8, 
        angularCycles=30, 
        interpolate=False,
        autoLog=False
    )

except (RuntimeError, TypeError, NameError):
    pass

arrow = visual.ImageStim(
    win,
    image="arrow.png",
    size=[-2, 2],
    ori=0
)

obs_rot_rate = rotation_total_angle / (framerate_r * obs_time)
stim = wedge1
frame = -1
while not event.getKeys(keyList=['q'], timeStamped=False):
    frame += 1
    wedge_cover.ori -= obs_rot_rate
    if frame % frame_spacing == 0:
            print("flip")
            if stim == wedge1:
                stim = wedge2
            else: 
                stim = wedge1

    # stim.draw()
    outer.draw()
    wedge_cover.draw()
    inner.draw()
    timebar_background.draw()
    arrow.draw()
    win.flip()

win.close()
core.quit()