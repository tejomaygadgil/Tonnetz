import ctcsound
import Tonnetz as tz
from random import randint, random
import numpy as np
from math import sin, pi

def midi2pch(num):
    "Convert MIDI Note Numbers to Csound PCH format"
    return "%d.%02g" % (3 + (num / 12), num % 12)

# Our Orchestra for our project
orc = """
sr=44100
ksmps=32
nchnls=2
0dbfs=1

instr 1 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.15, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 400 + (0.5 * kenv), .6
outs aout, aout
endin

instr 2 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.15, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 400 + (0.5 * kenv), .6
outs aout, aout
endin


instr 3 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.15, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 400 + (0.5 * kenv), .6
outs aout, aout
endin
"""

i_data = []
c = tz.Tonnetz()
i_data.append(c.pch)
c.r
i_data.append(c.pch)
c.p
i_data.append(c.pch)
c.r
i_data.append(c.pch)

for i in range(64*2):
   i_data.append(str("i 1 ") + str(i * .125) + " " + str(.25) + " " + i_data[i // 32][i % 3])

# seqLength = 9
# seq = list(np.random.choice(list(filter(lambda x: x % 12 in [0, 4, 7, 11], range(50,90))), seqLength))
# seq = list(filter(lambda x: x % 12 in [0, 4, 7, 11], range(50,90)))[:seqLength]
# i_data = []
# for i in range(32):
#     i_data.append(str("i 1 ") + str(i * .125) + " " + str(.25) + " " + seq[i % seqLength])

# t_amt = [-12, -1, -17]
# i_data = []
# for i in range(64):
#     i_data.append(Note(1, i * .125, .25, sin(pi * i / 8), 
#         t_amt[0] * (i >= 16 and i < 32) + t_amt[1] * (i >= 32 and i < 48) + t_amt[2] * (i >= 48) + seq[i % seqLength]))

# now convert list of Note objects to string
sco = ""
for n in i_data:
    sco += "%s\n"%n # this implicitly calls the __str__ method on the Note Class

# sco = "r2\n" + sco + "e"


print('Here is the list of score events that was generated:')
print()
print(sco)

c = ctcsound.Csound()    # create an instance of Csound
c.setOption("-odac")  # Set option for Csound
c.compileOrc(orc)     # Compile Orchestra from String
c.readScore(sco)     # Read in Score generated from notes 
c.start()             # When compiling from strings, this call is necessary before doing any performing

# The following is our main performance loop. We will perform one block of sound at a time 
# and continue to do so while it returns 0, which signifies to keep processing.  

while (c.performKsmps() == 0):
  pass

c.reset()
