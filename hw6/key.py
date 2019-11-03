###############################################################################

from .pitch import Pitch
from .mode import Mode
from .interval import Interval


## A class that implements musical keys.
#
# The Key class represents the complete chromatic set of keys in western music.
# A key consists of an integer 'signum' representing the number of sharps or
# flats in the key's signature, and a mode (Enum). Keys can return Pnums
# representing their tonic note and diatonic scale degrees.
# See: https://en.wikipedia.org/wiki/Key_(music)
class Key:
    ## Creates a Key from an integer key signature identifier and mode.
    #  @param signum  A value -7 to 7 representing the number of flats
    #  (negative) or sharps (positive).
    #  @param mode  A Mode enum, or its case-insensitive string name.
    #
    #  The constructor should raise a TypeError if signum is not an integer
    #  or if mode is not a Mode or string. The constructor should raise a
    #  ValueError if the signum integer or the mode string is invalid.
    modeNames = ['Major',
                 'Dorian',
                 'Phrygian',
                 'Lydian',
                 'Mixolydian',
                 'Minor',
                 'Locrian'
                 ]

    keys = {-7: Pitch('Cf0').pnum(),
            -6: Pitch('Gf0').pnum(),
            -5: Pitch('Df0').pnum(),
            -4: Pitch('Af0').pnum(),
            -3: Pitch('Ef0').pnum(),
            -2: Pitch('Bf0').pnum(),
            -1: Pitch('F0').pnum(),
            0: Pitch('C0').pnum(),
            1: Pitch('G0').pnum(),
            2: Pitch('D0').pnum(),
            3: Pitch('A0').pnum(),
            4: Pitch('E0').pnum(),
            5: Pitch('B0').pnum(),
            6: Pitch('Fs0').pnum(),
            7: Pitch('Cs0').pnum()
            }

    modeTranspose = {'Major': Interval('P1'),
                 'Dorian': Interval('M2'),
                 'Phrygian': Interval('M3'),
                 'Lydian': Interval('P4'),
                 'Mixolydian': Interval('P5'),
                 'Minor': Interval('M6'),
                 'Locrian': Interval('M7')}

    majorIntervals = {Interval('M2'),Interval('M2'),Interval('m2'),Interval('M2'),Interval('M2'),Interval('M2'),Interval('m2')}
    dorianIntervals = majorIntervals[1:] + majorIntervals[:1]
    phrygianIntervals = majorIntervals[1:] + majorIntervals[:1]
    lydianIntervals = majorIntervals[1:] + majorIntervals[:1]
    mixolydianIntervals = majorIntervals[1:] + majorIntervals[:1]
    minorIntervals = majorIntervals[1:] + majorIntervals[:1]
    locrianIntervals = majorIntervals[1:] + majorIntervals[:1]

    def __init__(self, signum, mode):
        if (isinstance(signum, int)):
            self.signum = signum
            if (mode in Key.modeNames):
                self.mode = mode
            elif mode == "Ionian":
                self.mode = mode[0]
            elif mode == "Aeolian":
                self.mode = mode[5]
        else:
            raise ValueError("signum must be an int")


    ## Returns the print representation of the key. The string should
    # include the class name, tonic, mode, number of sharps or flats,
    # and the instance id.
    #
    # Examples:
    # <Key: C-Major (0 sharps or flats) 0x10c03c050>
    # <Key: G-Major (1 sharp) 0x10eec5250>
    # <Key: A-Mixolydian (2 sharps) 0x10c03c490>
    # <Key: Af-Minor (7 flats) 0x10c03c390>
    def __str__(self):
        if self.signum < 0:
            return f'Key: {self.string()} ({abs(self.signum)} flat(s)) {hex(id(self))}'
        elif self.signum > 0:
            return return f'Key: {self.string()} ({abs(self.signum)} sharp(s)) {hex(id(self))}'
        else:
            return return f'Key: {self.string()} ({abs(self.signum)} sharps or flats) {hex(id(self))}'

    ## Returns the external representation of the Key including the
    # constructor name, signum, and the capitalized version of the
    # mode's name.
    #
    # Examples:
    # 'Key(4, "Dorian")'
    # 'Key(-1, "Major")'
    def __repr__(self):
        return f'Key({self.signum}, "{self.mode}")'

    ## Returns a string containing the name of the tonic Pnum, a
    # hyphen, and the capitalized version of the mode's name.
    #
    # Examples: Fs-Dorian, Bf-Phrygian, B-Major
    def string(self):
        for value in Key.keys:
            if value == self.signum:
                return f'{str(value)}-{self.mode}'

    ## Returns a Pnum representing the key's tonic. The tonic can
    # be calculated by transposing the Major tonic (Pnum) by the
    # interval distance of the mode above the major. The
    # transposition can be performed using that interval's transpose()
    # method. The interval distances of Major up to Locrian are:
    # P1, M2, M3, P4, P5, M6, M7.
    #
    # Examples:
    # Key(0, "lydian").tonic() is Pnum F.
    # Key(2, "dorian").tonic() is Pnum E.
    # Key(-6, "phrygian").tonic() is Pnum Bf.
    def tonic(self):
        if self.signum in Key.keys:
            return Key.modeTranspose.get(self.mode).transpose(Key.get(self.signum))

    ## Returns a list of Pnums representing the unique pitches of the key's
    # diatonic scale. The octave completion should NOT be included in the list.
    def scale(self):
        if self.mode == "Major":
            return [i.transponse(Key.keys.get(self.signum)) for i in Key.majorIntervals]


