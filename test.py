from psychopy import prefs
# prefs.hardware['audioLib'] = ['pygame']
# prefs.hardware['audioLib'] = ['sounddevice']
prefs.hardware['audioLib'] = ['pyo']
# prefs.general['winType'] = 'glfw'

from psychopy import visual, core, event
from psychopy.sound import Sound
# from psychopy.data import TrialHandler
from os import listdir, path

import egi.simple as egi
# reload(egi)

import sys
import time

ms_localtime = egi.ms_localtime

ns = egi.Netstation()
ns.connect('10.10.10.42', 55513)
ns.BeginSession()
#
ns.sync()
#
ns.StartRecording()
#
# sampleDir = "./samples"
#
# sampleFilenames = [path.join(sampleDir, f) for f in listdir(sampleDir)]

# psychopy.voicekey.samples_from_file(sampleFilenames[0])

# trials = TrialHandler(sampleFilenames, 1, method="random")
s = Sound()

win = visual.Window()
msg = visual.TextStim(win, text="Press a key to hear a sound, Q to quit")

s.setSound("./samples/13.wav")
while True:
	msg.draw()
	win.flip()
	k = event.getKeys()
	if len(k)>0:
		if 'q' in k:
			break
		ns.sync()
		s.play()
		ns.send_event('evt1')
		time.sleep(0.1)
	event.clearEvents()

ns.send_event('evt5', timestamp=egi.ms_localtime())

# for trial in trials:
# 	s.setSound(trial)
# 	while True:
# 		msg.draw()
# 		win.flip()
# 		if len(event.getKeys())>0:
# 			event.clearEvents()
# 			s.play()
# 			break
# 		event.clearEvents()

core.wait(1)
win.close()

ns.StopRecording()

ns.EndSession()
ns.disconnect()

# s = Sound()

# s.setSound("")
# s.play()
