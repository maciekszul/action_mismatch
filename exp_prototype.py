# exp dev

from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
import psychopy.tools.coordinatetools as ct
from psychopy.iohub import launchHubServer
from psychopy.hardware import joystick
import numpy as np


# monitor settings
x230 = (56, 56, (1366, 768))

width, dist, res = x230

mon = monitors.Monitor("default")
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)

win = visual.Window(size=res,
                    color="#000000",
                    fullscr=True,
                    allowGUI=False,
                    winType="pyglet",
                    units="deg",
                    monitor=mon)

# hardware settings

joyN = joystick.getNumJoysticks()
joy = joystick.Joystick(0)

# cue

sz = 0.15
th = sz/10.

circle = visual.Circle(win,
                       radius=sz,
                       edges=40,
                       units='deg',
                       fillColor='white',
                       lineColor='white')

line1 = visual.ShapeStim(win,
                         vertices=[[sz, 0 + th],
                                   [-sz*2, 0 + th],
                                   [-sz*2, 0 - th],
                                   [sz*2, 0 - th]],
                         units='deg',
                         fillColor='black',
                         lineColor='black')

line2 = visual.ShapeStim(win,
                         vertices=[[0 - th, sz*2],
                                   [0 + th, sz*2],
                                   [0 + th, -sz*2],
                                   [0 - th, -sz*2]],
                         units='deg',
                         fillColor='black',
                         lineColor='black')

circle1 = visual.Circle(win,
                        radius=th,
                        edges=40,
                        units='deg',
                        fillColor='white',
                        lineColor='white')


def draw_cue():
    circle.draw()
    line1.draw()
    line2.draw()
    circle1.draw()



# stim
text_stim = visual.TextStim(
    win,
    text="",
    height=0.5,
    color="#808080",
    pos=(-28, 14.5),
    alignHoriz="left"
)
outer = visual.Circle(win, 10, edges=100)
line = visual.Line(win, start=(0.0, 0.0), end=(10.0, 0.0))
ball = visual.Circle(
    win, 
    1,
    edges=20,
    fillColor="white",
    lineColor="white",
    pos=[10,0]
)


# exp
x, y = joy.getX(), -joy.getY()
theta0, radius = ct.cart2pol(x, y, units="rad")
theta_start = theta0
check = False

event.clearEvents()

while not event.getKeys(keyList=['q'], timeStamped=False):
    
    if event.getKeys(keyList=['i'], timeStamped=False):
        check = True
    elif event.getKeys(keyList=['c'], timeStamped=False):
        check = False
    
    x, y = joy.getX(), -joy.getY()
    
    theta, radius = ct.cart2pol(x, y, units="rad")
    theta_delta = theta-theta0
    
    if radius > 0.25 and np.abs(theta) < 2:
        theta_delta = theta-theta0
    if check:
        theta_start = theta_start - (theta_delta ) # oddball conditions
    else:
        theta_start = theta_start + (theta_delta) # regular
    
    ball.pos = ct.pol2cart(theta_start, 10, units="rad")
    ball.draw()

    outer.draw()

    text_stim.text = "X:{}\nY: {}\nANG: {}\nRAD: {}\ndelta ANG: {}".format(x,y, theta+np.pi, radius, theta_delta)
    text_stim.draw()
    
    win.flip()
    
    theta0 = theta

win.close()
core.quit()