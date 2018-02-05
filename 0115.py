from time import sleep
import mido
import Tonnetz as t

# outport = mido.open_output('LoopBe Internal MIDI 1')
# outport.send(mido.Message('note_on', channel=1, note=60))

def Yo(FL = 0, channel = 1, bpm = 0):
	if FL==1: outport = mido.open_output('LoopBe Internal MIDI 1')
	else: outport = mido.open_output()

	def toSec(bpm, div=1):
		return bpm / (60 * div)
	def play(notes, channel):
		for i in list(notes): outport.send(mido.Message('note_on', channel=channel, note=i))
	def rest(sec): sleep(sleepT)
	c = t.makeChord()

	bps = toSec(bpm)
	running = True
	mute = False
	stack = False
	while running==True:
		line = input('Wat u want> ')
		for i in list(line):
			if i == 'q':
				print('k bye')
				running = False
				outport.close()
			elif i == 't': c.t(int(input('amt? ')))
			elif i == 'm': bps = toSec(int(input('New bpm? ')))
			elif i == '<': stack = True
			elif i == '>': stack = False
			elif i == '(': mute = True
			elif i == ')': mute = False
			else:
				if i == 'i': c = t.makeChord()
				elif i == 'p': c.p
				elif i == 'l': c.l
				elif i == 'r': c.r
				elif i == 'n': c.n
				elif i == 's': c.s
				elif i == 'h': c.h
				print(c)
				if mute == False: play(c.notes, channel)
				if stack == False: rest(bps)