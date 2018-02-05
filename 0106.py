from Tonnetz import Tonnetz
from Verticals import seq, Verticals
import ctcsound
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

def norm(arr, x=1):
	arr = [(max(arr) - v) for v in arr][:]
	arr = [v/max(arr) for v in arr] 
	return [int((x) * v) for v in arr]

def csoundChords(t, trnArr, keyArr, keyVec):
	t.p
	i_data = []
	for i in range(len(trnArr)):
		if(trnArr[i % 5]==0): t.p
		elif(trnArr[i % 5]==1): t.l
		elif(trnArr[i % 5]==2): t.r
		elif(trnArr[i % 5]==3): t.n
		elif(trnArr[i % 5]==4): t.s
		elif(trnArr[i % 5]==5): t.h
		t.t(keyVec[keyArr[i]], abs=1)
		i_data.append(t.pch)
	return i_data

# import image
imDir = 'C:\\Users\\Tejomay Gadgil\\Dropbox\\neo_rem\\Tonnetz\\image.jpg'
lines = np.flipud(io.imread(imDir))[:,::-1]
# create regions
trnIm = lines[0:lines.shape[0]//2]
keyIm = lines[lines.shape[0]//2:lines.shape[0]]

seqLength = 16
# process transformation type
trnInd = seq(666, 3500, seqLength)
trnRaw = Verticals(trnIm, trnInd)
trn = norm(trnRaw,4)

plt.figure(figsize=(20, 20))
plt.imshow(trnIm)
plt.scatter(trnInd, trnRaw)
plt.show()
print(trnInd, trnRaw)
print(trn)
# process key
keyInd = seq(600, 3500, seqLength * 2)
keyRaw = Verticals(keyIm, keyInd)
keys = [12, 4, 11, 4, 7, 11, 12, 17, 14, 16, 12, 4, 7, 11, 12, 12, 15, 17, 12, 24]
key = norm(keyRaw, len(keys) - 1)

plt.figure(figsize=(20, 20))
plt.imshow(keyIm)
plt.scatter(keyInd, keyRaw)
plt.show()
print(keyInd, keyRaw)
print(key)

chord = Tonnetz()
chords = csoundChords(chord, trn, key, keys)

i_data = []
for i in range(len(chords)):
	for j in range(3):
		i_data.append(str("i " + str(j + 1) + " " + str(i) + " " + str(.25) + " " + str(chords[i][j])))

sco = ""
for n in i_data: sco += "%s\n"%n

orc = """
sr=44100
ksmps=32
nchnls=2
0dbfs=1

instr 1 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.6, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 1200 + (0.5 * kenv), .6
outs aout, aout
endin

instr 2 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.6, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 1200 + (0.5 * kenv), .6
outs aout, aout
endin


instr 3 
ipch = cps2pch(p4, 12)
kenv linsegr 1, 0.6, .1, .6, 0
aout vco2 0.3 * kenv, ipch
aout moogladder aout, 1200 + (0.5 * kenv), .6
outs aout, aout
endin
"""

print('Here is the list of score events that was generated:')
print()
print(sco)

c = ctcsound.Csound()    # create an instance of Csound
c.setOption("-odac")  # Set option for Csound
c.compileOrc(orc)     # Compile Orchestra from String
c.readScore(sco)     # Read in Score generated from notes 
c.start()             # When compiling from strings, this call is necessary before doing any performing

while (c.performKsmps() == 0):
  pass

c.reset()
