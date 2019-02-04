from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import numpy as np
import misc


# exp settings
background_color = "#A9A9A9"
exp_gray = "#A1A1A1"

wedge_rad = [0, 45]
wedge_size = 20

fix_time = 0.5
rot_time = 1.2
blink = 0.1
obs_time = 0.7
ITI = (500, 900)

trial_no = 10
prop_dev = 0.5

# time bar background shape
bar_h = 2
bar_w = 0.2
bar_shape = [
    [-(bar_w/2), -(bar_h/2)],
    [-(bar_w/2), (bar_h/2)],
    [(bar_w/2), (bar_h/2)],
    [(bar_w/2), -(bar_h/2)]
]

# time bar
tbar_h = 2
tbar_w = 0.2
tbar_shape = bar_shape

# prompt
exp_info = {
    "ID": 0,
    "age": 0,
    "gender (m/f/o)": "o",
    "exp type (prc/exp)": "exp",
}

prompt = gui.DlgFromDict(
    dictionary=exp_info, 
    title="Action Preception Mismatch"
)

subject = exp_info["ID"]
age = exp_info["age"]
gender = exp_info["gender (m/f/o)"]
exp_type = exp_info["exp type (prc/exp)"]

# monitor settings
x230 = (56, 56, (1366, 768))

width, dist, res = x230

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

# hardware settings
# joyN = joystick.getNumJoysticks()
# joy = joystick.Joystick(0)


# stim
inner = visual.Circle(
    win, 
    1, 
    edges=100, 
    fillColor=background_color, 
    lineColor=background_color
)

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
    fillColor="red"
)

try:
    wedge0 = visual.RadialStim(
        win, 
        color=exp_gray, 
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
        tex="sqrXsqr", 
        color=-1, 
        size=wedge_size,
        visibleWedge=wedge_rad, 
        radialCycles=4, 
        angularCycles=8, 
        interpolate=False,
        autoLog=False
    )
except TypeError:
    pass

# cue

sz = 0.15
th = sz / 10

circle = visual.Circle(
    win,
    radius=sz,
    edges=40,
    units="deg",
    fillColor="white",
    lineColor="white"
)


inner = visual.Circle(
    win, 
    1, 
    edges=100, 
    fillColor=background_color, 
    lineColor=background_color
)

line1 = visual.ShapeStim(
    win,
    vertices=[
        [sz, 0 + th],
        [-sz*2, 0 + th],
        [-sz*2, 0 - th],
        [sz*2, 0 - th]
    ],
    units='deg',
    fillColor='black',
    lineColor='black'
)

line2 = visual.ShapeStim(
    win,
    vertices=[
        [0 - th, sz*2],
        [0 + th, sz*2],
        [0 + th, -sz*2],
        [0 - th, -sz*2]
    ],
    units='deg',
    fillColor='black',
    lineColor='black'
)

circle1 = visual.Circle(
    win,
    radius=th,
    edges=40,
    units='deg',
    fillColor='white',
    lineColor='white'
)

def draw_cue():
    circle.draw()
    line1.draw()
    line2.draw()
    circle1.draw()

exp_sequence = misc.oddball_sequence(trial_no, prop_dev)

np.round(framerate)

# EXPERIMENT'

for stim_mode in exp_sequence:
    draw_cue()
    for frame in np.arange(np.round(framerate) // fix_time):
        win.flip()


win.close()
core.quit()