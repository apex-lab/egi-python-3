from psychopy import prefs
# prefs.hardware['audioLib'] = ['pygame']
# prefs.hardware['audioLib'] = ['sounddevice']
# prefs.hardware['audioLib'] = ['pyo']
# prefs.general['winType'] = 'glfw'

from psychopy import visual, core, event
# from psychopy.sound import Sound
# from psychopy.data import TrialHandler
import rtmixer
import sounddevice as sd
import soundfile as sf
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
# s = Sound()

win = visual.Window()
msg = visual.TextStim(win, text="Press a key to hear a sound, Q to quit")

playback_blocksize = None
latency = None
reading_blocksize = 1024  # (reading_blocksize * rb_size) has to be power of 2
rb_size = 16  # Number of blocks

def play_file(filename):
	with sf.SoundFile(filename) as f:
	    with rtmixer.Mixer(channels=f.channels,
	                       blocksize=playback_blocksize,
	                       samplerate=f.samplerate, latency=latency) as m:
	        elementsize = f.channels * m.samplesize
	        rb = rtmixer.RingBuffer(elementsize, reading_blocksize * rb_size)
	        # Pre-fill ringbuffer:
	        _, buf, _ = rb.get_write_buffers(reading_blocksize * rb_size)
	        written = f.buffer_read_into(buf, dtype='float32')
	        rb.advance_write_index(written)
	        action = m.play_ringbuffer(rb)
	        while True:
	            while rb.write_available < reading_blocksize:
	                if action not in m.actions:
	                    break
	                sd.sleep(int(1000 * reading_blocksize / f.samplerate))
	            if action not in m.actions:
	                break
	            size, buf1, buf2 = rb.get_write_buffers(reading_blocksize)
	            assert not buf2
	            written = f.buffer_read_into(buf1, dtype='float32')
	            rb.advance_write_index(written)
	            if written < size:
	                break
	        m.wait(action)
	        if action.done_frames != f.frames:
	            RuntimeError('Something went wrong, not all frames were played')
	        if action.stats.output_underflows:
	            print('output underflows:', action.stats.output_underflows)


# s.setSound("./samples/13.wav")
while True:
	msg.draw()
	win.flip()
	k = event.getKeys()
	if len(k)>0:
		if 'q' in k:
			break
		ns.sync()
		play_file("./samples/13.wav")
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
