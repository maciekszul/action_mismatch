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

outer = visual.Circle(win, 10, edges=100)
line = visual.Line(win, start=(0.0, 0.0), end=(10.0, 0.0))
ball = visual.Circle(win, 1,
                     edges=20,
                     fillColor="white",
                     lineColor="white")


# exp

event.clearEvents()
check = False
while not event.getKeys(keyList=['q'], timeStamped=False):
    x, y = joy.getX(), joy.getY()
    if event.getKeys(keyList=['i'], timeStamped=False):
        check = True
    elif event.getKeys(keyList=['c'], timeStamped=False):
        check = False
    if check:
        theta, radius = ct.cart2pol(x, y, units="deg")
        ball.pos = ct.pol2cart(theta, 10, units="deg")
    else:
        theta, radius = ct.cart2pol(x, -y, units="deg")
        ball.pos = ct.pol2cart(theta, 10, units="deg")

    ball.draw()
    outer.draw()
    draw_cue()
    win.flip()


win.close()
core.quit()