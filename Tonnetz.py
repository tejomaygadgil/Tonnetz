scaleDict = dict(zip(["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"],list(range(12))))

class Tonnetz:
    def __init__(self, notes, order):
        self.notes = notes[:]
        self.order = order[:]
    def __str__(self):
        scale = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
        notesNamed = [scale[i % 12] + str(i // 12) for i in self.notes]
        return str(notesNamed[self.order[0]] + " " + self.quality + " - " + str(notesNamed))
    def __repr__(self):
        return self.__str__()
    @property
    def quality(self):
        interval = (self.notes[self.order[1]] - self.notes[self.order[0]]) % 12
        if   interval == 4: return 'maj'
        elif interval == 3: return 'min'
        else:               return 'idk'
    def pch(self):
        pch_list = []
        for i in self.notes:
            pch_list.append("%d.%02g" % (2 + (i / 12), i % 12))
        return pch_list
    # Transpose
    def t(self, amt):
        """Transpose chord by amt."""
        self.notes = [i + amt for i in self.notes]
    def NRTran(self, major_tran, minor_tran):
        if   self.quality == 'maj': t_order, t_amt, r_order = major_tran[:]
        elif self.quality == 'min': t_order, t_amt, r_order = minor_tran[:]
        # transpose note
        self.notes[self.order[t_order]] += t_amt
        # update root
        if r_order != 0:
            newRoot = self.notes[self.order[r_order]]
            self.order = [i[0] for i in sorted(enumerate([(i - newRoot) % 12 for i in self.notes]), key = lambda x: x[1])]
    @property
    def p(self):
        """Apply P-transformation to chord."""
        # major triad -> decrement 2nd note by one semitone (III->IIIb)
        # minor triad -> increment 2nd note by one semitone (III->III#)
        self.NRTran(major_tran = [1, -1, 0], minor_tran = [1, 1, 0])
        return self
    @property
    def l(self):
        """Apply L-transformation to chord."""
        # major triad -> decrement 1st note by one semitone (I->Ib) and update root to 2nd note
        # minor triad -> increment 3rd note by one semitone (V->V#) and update root to 3rd note
        self.NRTran(major_tran = [0, -1, 1], minor_tran = [2, 1, 2])
        return self
    @property
    def r(self):
        """Apply R-transformation to chord."""
        # major triad -> increment 3rd note by two semitones (V->VI)  and update root to 3rd note
        # minor triad -> decrement 1st note by two semitones (I->VI#) and update root to 3rd note
        self.NRTran(major_tran = [2, 2, 2], minor_tran = [0, -2, 1])
        return self
    @property
    def n(self):
        """Return N-transformed chord."""
        self.r.l.p
        return self
    @property
    def s(self):
        """Return S-transformed chord."""
        self.l.p.r
        return self
    @property
    def h(self):
        """Return H-transformed chord."""
        self.l.p.l
        return self
 
# Constructor
def makeChord(root=0, quality=2):
    triadList = ((0, 3, 7), (0, 4, 6), (0, 4, 7), (0, 4, 8))
    return Tonnetz([i + 60 + root for i in triadList[quality]], [0, 1, 2])



# a chord is a point on a topology
# a progression has a collection of points 

# # class progression():
# #     """ A progresssion has chords.
# #     """
# #     def __init__(self):
# #         self.chords = []
# #     def addChord(self, chord):
# #         self.chords.append(chord)
# #     def export(self):
# #         return [i.notes for i in self.chords]
# """


# freq = [27.5 * ((2**(1.0 / 12.0))**i) for i in range(88)]

# for i in range(0,88,12):
#     print("(A" + str(i // 12) + "): " + str(freq[i] // 1))
#     print("(A%d): %.1f" % (i/12,freq[i]))


# def ops(**dic):
#     x = dic['x']
#     y = dic['y']
#     return x + y, x - y, x * y, x / y

# for i in range(1,88):
#     freq.append(freq[i-1]*(2**(1.0 / 12.0)))


