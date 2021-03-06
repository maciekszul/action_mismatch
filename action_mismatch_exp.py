from __future__ import division
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

try:
    from pypixxlib.propixx import PROPixxCTRL
    pxctrl = PROPixxCTRL()
    px_out = pxctrl.dout

except ImportError:
    class dummy:
        def setBitValue(self, value=0, bit_mask=0xFF):
            pass

        def updateRegisterCache(self):
            pass
    pxctrl = dummy()
    px_out = dummy()

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

# eyetracker setup

iohub_tracker_class_path = 'eyetracker.hw.sr_research.eyelink.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
eyetracker_config['enable'] = True
eyetracker_config['stream_events'] = False
eyetracker_config['model_name'] = 'EYELINK 1000 TOWER'
eyetracker_config['default_native_data_file_name'] = subj_ID
eyetracker_config['simulation_mode'] = True
eyetracker_config['runtime_settings'] = dict(sampling_rate=1000,
                                             track_eyes='RIGHT')

try:
    from psychopy.iohub import launchHubServer

    io = launchHubServer(**{iohub_tracker_class_path: eyetracker_config})

    tracker = io.devices.tracker

    r = tracker.runSetupProcedure()

except:
    class another_dummy():
        def sendMessage(self, x):
            pass
        
        def quit():
            pass
    
    tracker = another_dummy()
    io = another_dummy()

def trigger(bit, t):
    """
    triggers ProPixxControl
    returns trigger time, start and end of the function
    """
    start = core.getTime()
    wait = core.StaticPeriod()
    px_out.setBitValue(value=bit, bit_mask=0xFF)
    pxctrl.updateRegisterCache()
    wait.start(t)
    tracker.sendMessage(str(bit))
    trig = core.getTime()
    wait.complete()
    px_out.setBitValue(value=0, bit_mask=0xFF)
    pxctrl.updateRegisterCache()
    end = core.getTime()
    return (trig, start, end)


# exp settings
# background_color = "#c7c7c7"
background_color = "#939393"

# exp_gray = "#c2c2c2"
exp_gray = "#848484"

wedge_rad = [0, 90]
wedge_size = 20

rad_cyc = 4
ang_cyc = 15

fix_time = 0.5
rot_time = 1.5
blink_time = 0.1
obs_time = 1

flickering_freq = 16

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

# triggers
rot_dict = {
    1: 30,
    -1: 40,
    0: 50
}

obs_dict = {
    1: 60,
    -1: 70,
    0: 80
}

# 90 end of the trial, beginning of ITI
# 100 end of the ITI

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
    nMaxFrames=120,
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
    "ITI_dur",
    "trig_rot",
    "trig_obs"
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
        radialCycles=rad_cyc, 
        angularCycles=ang_cyc, 
        interpolate=False,
        autoLog=False
    )

    wedge2 = visual.RadialStim(
        win, 
        tex="sqrXsqr", 
        color=-1, 
        size=wedge_size,
        visibleWedge=[0,360], 
        radialCycles=rad_cyc, 
        angularCycles=ang_cyc, 
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

text_stim = visual.TextStim(
    win,
    text="",
    height=1,
    color="black",
    pos=(0, 0),
    alignHoriz="center"
)

# x, 15, 26%

exp_sequence = misc.oddball_sequence(no_chunks, no_elem, prop_dev)

instructions = [
    "Your task is to perform a circular movement (clockwise or anti-clockwise) within a designated time.\n\nTime is indicated by the red time bar in the center of the screen.",
    "Initiate it with an upward movement.\n\nMaintain the speed during the trial.\n\nCenter the joystick before the end of te time",
    "After the movement, observe the motion of the visual object.\n\nCount how many times the motion was different to the motion you performed."
    "Try to sit still during the trial.",
    "Head position measurement. Try to sit still.",
    "Experiment is starting after this message disappears."
]

for text in instructions:
    text_stim.text = text
    text_stim.draw()
    win.flip()
    event.waitKeys(
        maxWait=60, 
        keyList=["space"], 
        modifiers=False, 
        timeStamped=False
    )

# EXPERIMENT

tracker.setRecordingState(True)
tracker.sendMessage("START")

trigger(0, 0.005)

blank.draw()
win.flip()
core.wait(5)

exp_clock = clock.MonotonicClock()
exp_start = exp_clock.getTime()
for trial, stim_mode in enumerate(exp_sequence):
    exp_fix_onset = exp_clock.getTime()
    while True:
        x, y = joy.getX(), joy.getY()
        t, radius = ct.cart2pol(x, y, units="rad")
        if radius > 0.2:
            blank.draw()
            win.flip()
        else:
            break
    
    fix = core.StaticPeriod(screenHz=framerate_r)
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

    trig_rot, start, end = trigger(rot_dict[stim_mode], 0.005)
    
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
        if radius > 0.2:
            blank.draw()
            win.flip()
        else:
            break

    blink = core.StaticPeriod(screenHz=framerate_r)
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

    trig_obs, start, end = trigger(obs_dict[stim_mode], 0.005)

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
    trigger(90, 0.005)
    exp_iti_onset = exp_clock.getTime()
    ITI = core.StaticPeriod(screenHz=framerate_r)
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

    data_dict["trig_rot"].append(trig_rot)
    data_dict["trig_obs"].append(trig_obs)

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

    trigger(100, 0.005)

    if event.getKeys(keyList=['q'], timeStamped=False):
        break
        # win.close()
        # core.quit()

blank.draw()
win.flip()
core.wait(2)

instructions = [
    "End of the experiment"
]

for text in instructions:
    text_stim.text = text
    text_stim.draw()
    win.flip()
    event.waitKeys(
        maxWait=60, 
        keyList=["space"], 
        modifiers=False, 
        timeStamped=False
    )

tracker.sendMessage("END")
tracker.setRecordingState(False)
tracker.setConnectionState(False)

win.close()
io.quit()
core.quit()