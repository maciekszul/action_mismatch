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

# prompt
exp_info = {
    "ID": 0,
    "age": 0,
    "gender (m/f/o)": "o",
    "exp type (prc/exp)": "exp",
    "session": 1
}

prompt = gui.DlgFromDict(
    dictionary=exp_info, 
    title="Action Preception Mismatch"
)

subject = exp_info["ID"]
age = exp_info["age"]
gender = exp_info["gender (m/f/o)"]
exp_type = exp_info["exp type (prc/exp)"]
session = exp_info["session"]

subj_ID = str(subject).zfill(4)

timestamp = core.getAbsTime()

subj_dir = op.join("data/{}".format(subj_ID))
misc.mk_dir(subj_dir)

data_filename = "ses{}_{}_{}.csv".format(
    session,
    subj_ID,
    timestamp
)

joy_dir = op.join(subj_dir, data_filename[:-4])
misc.mk_dir(joy_dir)

# exp settings
background_color = "#c7c7c7"
exp_gray = "#c2c2c2"
# exp_gray = "#b8b8b8"

wedge_rad = [0, 90]
wedge_size = 15

fix_time = 0.5
rot_time = 1.5
blink_time = 0.1
obs_time = 1

flickering_freq = 8

ITI_bounds = (0.5, 0.9)

rotation_total_angle = 360

no_chunks = 1
no_elem = 10
prop_dev = 0.2

# time bar background shape
bar_h = 1.7
bar_w = bar_h/4
bar_shape = [
    [-(bar_w/2), -(bar_h/2)],
    [-(bar_w/2), (bar_h/2)],
    [(bar_w/2), (bar_h/2)],
    [(bar_w/2), -(bar_h/2)]
]

# time bar
tbar_h = 1.7
tbar_w = tbar_h/4
tbar_shape = bar_shape

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

# hardware settings
joyN = joystick.getNumJoysticks()
joy = joystick.Joystick(0)

# data logging settings
columns = [
    "ID",
    "age",
    "gender",
    "trial",
    "exp_type",
    "movement_dir",
    "obs_dir_mod",
    "fix_onset",
    "rot_onset",
    "blink_onset",
    "obs_onset",
    "ITI_onset",
    "fix_dur",
    "rot_dur",
    "blink_dur",
    "obs_dur",
    "ITI_dur"
]

data_dict = {i: [] for i in columns}

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

arrow = visual.ImageStim(
    win,
    image="arrow.png",
    size=[2,2],
    ori=0
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
    fillColor="red",
    lineColor="red"
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
        visibleWedge=[0,360], 
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
        visibleWedge=[0,360], 
        radialCycles=8, 
        angularCycles=30, 
        interpolate=False,
        autoLog=False
    )

except (RuntimeError, TypeError, NameError):
    pass

obs_rot_rate = rotation_total_angle / (framerate_r * obs_time)

print(obs_rot_rate)

blank = visual.TextStim(
    win,
    text=" ",
    opacity=0.0
)


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

line1 = visual.ShapeStim(
    win,
    vertices=[
        [sz, 0 + th],
        [-sz*2, 0 + th],
        [-sz*2, 0 - th],
        [sz*2, 0 - th]
    ],
    units='deg',
    fillColor=background_color,
    lineColor=background_color
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
    fillColor=background_color,
    lineColor=background_color
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

exp_sequence = misc.oddball_sequence(no_chunks, no_elem, prop_dev)


# EXPERIMENT'
blank.draw()
win.flip()
core.wait(2)

exp_clock = clock.MonotonicClock()
exp_start = exp_clock.getTime()
for trial, stim_mode in enumerate(exp_sequence):
    exp_fix_onset = exp_clock.getTime()

    while True:
        x, y = joy.getX(), joy.getY()
        t, radius = ct.cart2pol(x, y, units="rad")
        if radius > 0.1:
            blank.draw()
            win.flip()
        else:
            break
    
    fix = clock.StaticPeriod(screenHz=framerate_r)
    draw_cue()
    win.flip()
    fix.start(fix_time)
    # operations during fix
    fix.complete()
    exp_rot_onset = exp_clock.getTime()

    # first readout
    x, y = joy.getX(), -joy.getY()
    theta0, radius = ct.cart2pol(x, y, units="rad")

    movement_dir = []
    x_trial = [x]
    y_trial = [y]
    t_trial = [exp_rot_onset]
    for frame in np.arange((framerate_r * rot_time)):
        x, y = joy.getX(), joy.getY()
        x_trial.append(x)
        y_trial.append(y)
        t_trial.append(exp_clock.getTime())
        theta, radius = ct.cart2pol(x, y, units="rad")
            
        theta_delta = theta-theta0
        movement_dir.append(theta_delta)
        if radius > 0.2 and theta < 10:
            wedge_cover.ori = np.rad2deg(theta)

        outer.draw()
        wedge_cover.draw()
        inner.draw()
        timebar_background.draw()
        time_prop = 1 - frame/(framerate_r * rot_time)
        tbar_shape = [
            [-(tbar_w/2), -(tbar_h/2)],
            [-(tbar_w/2), -(tbar_h/2) + time_prop * bar_h],
            [(tbar_w/2), -(tbar_h/2) + time_prop * bar_h],
            [(tbar_w/2), -(tbar_h/2)]
        ]
        timebar_foreground.vertices = tbar_shape
        timebar_foreground.draw()
        if stim_mode == 0:
            arrow.draw()
        win.flip()
        theta0 = theta
        # print(theta)
    
    exp_blink_onset = exp_clock.getTime()

    while True:
        x, y = joy.getX(), joy.getY()
        t, radius = ct.cart2pol(x, y, units="rad")
        if radius > 0.1:
            blank.draw()
            win.flip()
        else:
            break

    blink = clock.StaticPeriod(screenHz=framerate_r)
    blink.start(blink_time)
    # operations during blink
    if stim_mode != 0:
        movement_summary = np.sign(np.average(np.sign(movement_dir)))
        wedge1.ori = np.rad2deg(theta)
        wedge2.ori = np.rad2deg(theta)
        wedge1.draw()
        wedge2.draw()
        inner.draw()
        timebar_background.draw()
    blink.complete()

    exp_obs_onset = exp_clock.getTime()
    
    if stim_mode != 0:
        win.flip()

        stim = wedge1
        for frame in np.arange(framerate_r * obs_time - 1):
            wedge_cover.ori += ((obs_rot_rate * movement_summary) * stim_mode)

            if frame % frame_spacing == 0:
                if stim == wedge1:
                    stim = wedge2
                else: 
                    stim = wedge1

            stim.draw()
            wedge_cover.draw()
            inner.draw()
            timebar_background.draw()
            win.flip()
        blank.draw()
        win.flip()
    else:
        pass
    exp_iti_onset = exp_clock.getTime()
    ITI = clock.StaticPeriod(screenHz=framerate_r)
    ITI_time = np.random.uniform(low=ITI_bounds[0], high=ITI_bounds[1])
    ITI.start(ITI_time)
    # operations during ITI

    data_dict["ID"].append(subject)
    data_dict["age"].append(age)
    data_dict["gender"].append(gender)
    data_dict["trial"].append(trial)
    data_dict["exp_type"].append(exp_type)
    data_dict["movement_dir"].append(np.average(np.sign(movement_dir)))
    data_dict["obs_dir_mod"].append(stim_mode)
    
    data_dict["fix_onset"].append(exp_fix_onset)
    data_dict["rot_onset"].append(exp_rot_onset)
    data_dict["blink_onset"].append(exp_blink_onset)
    data_dict["obs_onset"].append(exp_obs_onset)
    data_dict["ITI_onset"].append(exp_iti_onset)

    data_dict["fix_dur"].append(exp_rot_onset - exp_fix_onset)
    data_dict["rot_dur"].append(exp_blink_onset - exp_rot_onset)
    data_dict["blink_dur"].append(exp_obs_onset - exp_blink_onset)
    data_dict["obs_dur"].append(exp_iti_onset - exp_obs_onset)
    data_dict["ITI_dur"].append(ITI_time)

    data_DF = pd.DataFrame(data_dict)
    data_DF.to_csv(
        op.join(subj_dir, data_filename)
    )
   
    joystick_output =  np.vstack([np.array(x_trial), np.array(y_trial), np.array(t_trial)])
    jo_filename = "ses{}_{}_trial{}_{}.npy".format(
        session,
        subj_ID,
        str(trial).zfill(4),
        timestamp
    )
    np.save(
        op.join(joy_dir,jo_filename), 
        joystick_output
    )
    
    print(ITI.complete())

    if event.getKeys(keyList=['q'], timeStamped=False):
        break
        # win.close()
        # core.quit()

win.close()
core.quit()