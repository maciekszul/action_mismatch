from __future__ import division
from psychopy import visual
from psychopy import core
from psychopy import event
from psychopy import monitors
from psychopy.hardware import joystick
import psychopy.tools.coordinatetools as ct
import math


""" MONITOR """

tower = (40.8, 56, (1600, 1200))
lab = (52.128, 56, (1920, 1080))
meg = (0, 0, (0, 0))

width, dist, res = tower

mon = monitors.Monitor('default')
mon.setWidth(width)
mon.setDistance(dist)
mon.setSizePix(res)

win = visual.Window(size=res,
                    color='#000000',
                    fullscr=True,
                    allowGUI=False,
                    winType='pyglet',
                    units='deg',
                    monitor=mon)

""" VISUALS """

outer = visual.Circle(win, 10, edges=100)
inner = visual.Circle(win, 4, edges=50)
line = visual.Line(win, start=(0.0, 0.0), end=(10.0, 0.0))
ball = visual.Circle(win, 0.5,
                     edges=20,
                     fillColor='#FFFFFF',
                     lineColor='#FFFFFF')
tine = visual.ShapeStim(win, 
                        lineWidth=0.1, 
                        lineColor='#32cd32', 
                        vertices=((0.0,0.0),(0.0,0.0)), 
                        interpolate=False,
                        closeShape=False)
text = visual.TextStim(win, text=' ',
                       color='#FFFFFF',
                       units='deg',
                       height=1,
                       opacity=1.0)


""" JOYSTICK """

joyN = joystick.getNumJoysticks()
joy = joystick.Joystick(0)


""" FUNCTIONS """

def in_circle(center_x, center_y, radius, x, y):
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

""" TRAINING """

text.setText('Try to keep the white ball between inner and outer circle while performing circular movement.\nPress SPACE to continue.')
text.draw()
win.flip()
event.waitKeys(
    maxWait=60, 
    keyList=['space'], 
    timeStamped=False, 
    clearEvents=True
)

all_fr = 0
in_fr = 0
vertices = [(0.0,0.0)]
event.clearEvents()
while not event.getKeys(keyList=['q'], timeStamped=False):
    all_fr += 1
    x, y = joy.getX(), joy.getY()
    vertices.append((x*10, -y*10))
    theta, radius = ct.cart2pol(x, y, units="deg")
    # line.ori = math.degrees(theta)
    line.ori = theta
    ball.pos = (x*10, -y*10)
    if in_circle(0.0, 0.0, 0.4, x, y) or not in_circle(0.0, 0.0, 1, x, y):
        ball.setFillColor('#9C2A00')
        ball.setLineColor('#9C2A00')
    else:
        ball.setFillColor('#FFFFFF')
        ball.setLineColor('#FFFFFF')
        in_fr += 1
    tine.setVertices(vertices)
    tine.draw()
    inner.draw()
    outer.draw()
    line.draw()
    ball.draw()
    win.flip()

perc = round((in_fr / all_fr) * 100)
text.setText('You have kept the ball within boundaries for {0}% of time.\nPress SPACE to continue.'.format(perc))
text.draw()
win.flip()
event.waitKeys(maxWait='inf', keyList=['space'], timeStamped=False)


""" END """
win.close()
core.quit()