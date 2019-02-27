from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from psychopy import clock

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


# eyetracker setup

iohub_tracker_class_path = 'eyetracker.hw.sr_research.eyelink.EyeTracker'
eyetracker_config = dict()
eyetracker_config['name'] = 'tracker'
eyetracker_config['enable'] = True
eyetracker_config['stream_events'] = False
eyetracker_config['model_name'] = 'EYELINK 1000 TOWER'
eyetracker_config['default_native_data_file_name'] = 'P666'
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

# monitor settings
background_color = "#c7c7c7"

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
    height=0.5,
    color="#ffffff",
    pos=(0, 0),
    alignHoriz="center"
)


instructions = [
    "a",
    "b",
    "c"
]


for text in instructions:
    text_stim.text = text
    text_stim.draw()
    win.flip()
    event.waitKeys(
        maxWait=60, 
        keyList=["space"], 
        modifiers=False, 
        timeStamped=False, 
        clearEvents=True
    )

trigger(0, 0.005)
text_stim.text = ""
text_stim.draw()
win.flip()
core.wait(1)

draw_cue()
win.flip()
trigger(64, 0.005)

event.waitKeys(
    maxWait=2, 
    keyList=["]"], 
    modifiers=False, 
    timeStamped=False, 
    clearEvents=True
)

trigger(64, 0.005)

text_stim.text = ""
text_stim.draw()
win.flip()
event.waitKeys(
    maxWait=60, 
    keyList=["space"], 
    modifiers=False, 
    timeStamped=False, 
    clearEvents=True
)

win.close()
core.quit()
io.quit()