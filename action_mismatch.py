# exp dev

from psychopy import core
from psychopy import visual
from psychopy import monitors
from psychopy import gui
from psychopy import event
from psychopy.iohub import launchHubServer

import numpy as np


# monitor settings
x230 = (17.26, 56, (1366, 768))

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
                    gamma=0,
                    monitor=mon)

# stim
text = visual.TextStim(win, text=" ",
                        color="white",
                        units="deg",
                        height=1,
                        opacity=1.0,
                        name="cross",
                        alignHoriz="center",
                        alignVert="center")

text.text = "blabla"
text.draw()
win.flip()
core.wait(2)

# win.close()
core.quit()