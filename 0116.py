from time import sleep
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_ON
import Tonnetz

outport = open_midioutput()
channel = max(1, min(int(input("channel ?")), 16))

def play():
	c = Tonnetz.makeChord()
	wait = 1.7
	mute = False
	stack = False
	running = True
	while running == True:
		line = input('Wat u want> ')
		for i in list(line):
			if i == 'q':
				print('k bye')
				running = False
			elif i == "(": 
				mute = True
				print("MUTED: ")
			elif i == ")": 
				mute = False
				print(" ")
			elif i == "<": 
				stack = True
				print("STACKED:")
			elif i == ">": 
				stack = False
				sleep(wait)
				print(" ")
			elif i == "w": wait = float(input('new wait amt? '))
			else:
				if i == 'i': c = Tonnetz.makeChord()
				elif i == 't': c.t(int(input('amt? ')))
				elif i == 'p': c.p
				elif i == 'l': c.l
				elif i == 'r': c.r
				elif i == 'n': c.n
				elif i == 's': c.s
				elif i == 'h': c.h
				print(c, "\n")
				if mute == False: 
					for i in list(c.notes): 
						outport[0].send_message([NOTE_ON | (channel - 1), i, 64])
					if stack == False: sleep(wait)

play()

outport[0].close_port()
