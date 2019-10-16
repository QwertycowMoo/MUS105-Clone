###############################################################################
from enum import IntEnum
from math import pow


## A class that implements musical pitches.
#
# The Pitch class represent equal tempered pitches and returns information
# in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
# can be compared using standard math relations and maintain proper spelling
# when complemented or transposed by an Interval.




class Pitch:

    ## A class variable that holds an IntEnum of all possible letter-and-accidental
    #  combinations Cff up to Bss. Each pnum encodes its letter and accidental index
    #  as a one byte value 'llllaaaa', where 'llll' is its letter index 0-6, and
    #  'aaaa' is its accidental index 0-4.  You should set the pnums variable like this:
    #  pnum = IntEnum('Pnum', [tuple...]) where Pnum is the name of the enum class,
    #  [tuple...'] is a list of tuples, and each tuple is (enum_name, enum_val).
    #  The enum names are all possible combinations of pitch letters and accidentals
    #  e.g. 'Cff' upto  'Bss'.  Since the accidental character # is illegal as a
    #  python enum name be sure to use only the 'safe versions' of the accidental
    #  names: 'ff' upto 'ss'. The enum values are the one byte integers containing
    #  the letter and accidental indexes: (letter << 4) + accidental.
    # noteList = [l+a for l in ['C', 'D', 'E', 'F', 'G', 'A', 'B'] for a in ['ff','f','','s','ss']]
    # valueEnum = [x<<4 + y for x, y in enumerate([0, 1, 2, 3, 4, 5, 6])]
    letterDict = {0: 'C',
                  1: 'D',
                  2: 'E',
                  3: 'F',
                  4: 'G',
                  5: 'A',
                  6: 'B'}
    accDict = {0: 'bb',
               1: 'b',
               2: '',
               3: '#',
               4: '##'}
    revAccDict = {"bb": 0,
                  "ff": 0,
                  "f": 1,
                  "b": 1,
                  "n": 2,
                  "#": 3,
                  "s": 3,
                  "ss": 4,
                  "##": 4}
    octDict = {0: '00',
               1: '0',
               2: '1',
               3: '2',
               4: '3',
               5: '4',
               6: '5',
               7: '6',
               8: '7',
               9: '8',
               10: '9'}


    pnums = IntEnum('Pnum', [('Cff', 0b00000000),
                             ('Cf', 0b00000001),
                             ('C', 0b00000010),
                             ('Cs', 0b00000011),
                             ('Css', 0b00000100),
                             ('Dff', 0b00010000),
                             ('Df', 0b00010001),
                             ('D', 0b00010010),
                             ('Ds', 0b00010011),
                             ('Dss', 0b00010100),
                             ('Eff', 0b00100000),
                             ('Ef', 0b00100001),
                             ('E', 0b00100010),
                             ('Es', 0b00100011),
                             ('Ess', 0b00100100),
                             ('Fff', 0b00110000),
                             ('Ff', 0b00110001),
                             ('F', 0b00110010),
                             ('Fs', 0b00110011),
                             ('Fss', 0b00110100),
                             ('Gff', 0b01000000),
                             ('Gf', 0b01000001),
                             ('G', 0b01000010),
                             ('Gs', 0b01000011),
                             ('Gss', 0b01000100),
                             ('Aff', 0b01010000),
                             ('Af', 0b01010001),
                             ('A', 0b01010010),
                             ('As', 0b01010011),
                             ('Ass', 0b01010100),
                             ('Bff', 0b01110000),
                             ('Bf', 0b01110001),
                             ('B', 0b01110010),
                             ('Bs', 0b01110011),
                             ('Bss', 0b01110100)])

    ## Creates a Pitch from a string or list, if neither is provided
    #  an empty Pitch is returned.
    #  * Pitch(string) - creates a Pitch from a pitch name string.
    #  * Pitch([l, a, o]) - creates a Pitch from a three element
    #  pitch list containing a letter, accidental and octave index
    #  (see below).
    #  * Pitch() - creates an empty Pitch.
    #
    #  @param ref A pitch name string, a list of three pitch indexes, or None.
    #
    # The format of a Pitch name string is:
    # @code
    #  <pitch> :=  <letter>, [<accidental>], <octave>
    #  <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B'
    #  <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
    #  <2flat> := 'bb' | 'ff'
    #  <flat> := 'b' | 'f'
    #  <natural> := ''
    #  <sharp> := '#' | 's'
    #  <2sharp> := '##' | 'ss'
    #  <octave> := '00' | '0' | '1'  | '2'  | '3'  | '4'  | '5'  | '6'  | '7'  | '8'  | '9'
    # @endcode
    #
    # The format of a three-element pitch list is:
    # * A letter index 0-6 corresponding to the pitch letter names ['C', 'D', 'E', 'F', 'G', 'A', 'B'].
    # * An accidental index 0-4 corresponding to symbolic accidental names ['bb', 'b', '', '#', '##']
    #   or 'safe' accidental names ['ff', 'f', '', 's', 'ss'].
    # * An octave index 0-10 corresponding to the pitch octave names ['00', '0', '1', '2', '3',
    #   '4', '5', '6', '7', '8', '9'].
    #
    # If the argument is not a pitch string, a pitch list, or None the method
    # should raise a TypeError.  If the string or list contains invalid information the
    # method should raise a ValueError.
    #
    # Examples: Pitch('C4'), Pitch('F##2'), Pitch('Gs8'), Pitch('Bb3'), Pitch("Df00"),
    # Pitch([0,3,6]), Pitch()

    def __init__(self, ref=None):
        letterDict = {'C': 0,
                      'D': 1,
                      'E': 2,
                      'F': 3,
                      'G': 4,
                      'A': 5,
                      'B': 6, }

        ## A letter index 0-6.
        if ref is None:
            self.letter = None
            self.octave = None
            self.accidental = None
        elif isinstance(ref, str):

            pitchList = list(ref)
            octaveIndex = 1
            #letter
            self.letter = letterDict.get(pitchList[0].upper(), "none")
            if self.letter == "none":
                raise ValueError("This is not a valid pitch")
            #accidental

            if pitchList[1] == '#' or pitchList[1] == 's':
                # if "##"
                if pitchList[2] == '#' or pitchList[2] == 's':
                    self.accidental = 4
                    octaveIndex = 3
                # if "#"
                else:
                   self.accidental = 3
                   octaveIndex = 2
            # if flats
            elif pitchList[1] == 'b' or pitchList[1] == 'f':
                # if 'bb'
                if pitchList[2] == 'b' or pitchList[2] == 'f':
                    self.accidental = 0
                    octaveIndex = 3
                # if 'b'
                else:
                    self.accidental = 1
                    octaveIndex = 2
            else:
                self.accidental = 2


            octaveStr = ''.join(pitchList[octaveIndex:])
            #octave
            if pitchList[octaveIndex] == '0':
                if ''.join(pitchList[octaveIndex:]) == '00':
                    self.octave = 0
                else:
                    self.octave = 1
            elif octaveStr.isdigit():
                if int(octaveStr) < 10 and int(octaveStr) > 0:
                    self.octave = int(pitchList[octaveIndex]) + 1
                else:
                    raise ValueError("This is not a valid pitch")
            else:
                raise ValueError("This is not a valid pitch")
            if self.keynum() > 127 or self.keynum() < 0:
                raise ValueError("This is not a valid pitch")

        elif isinstance(ref, list):
            if len(ref) > 3:
                raise ValueError("This is not a valid pitch")
            if ref[0] <= 6 and ref[0] >= 0:
                self.letter = ref[0]
                if ref[1] <= 4 and ref[1] >= 0:
                    self.accidental = ref[1]
                    if ref[2] <= 10 and ref[2] >= 0:
                        self.octave = ref[2]
                    else:
                        raise ValueError("This is not a valid pitch")
                else:
                    raise ValueError("This is not a valid pitch")
            else:
                raise ValueError("This is not a valid pitch")
            if self.keynum() > 127 or self.keynum() < 0:
                raise ValueError("This is not a valid pitch")
        else:
            raise ValueError("This is not a valid pitch")


    ## Returns a string displaying information about the
    #  pitch within angle brackets. Information includes the
    #  the class name, the pitch text, and the id of the object,
    #  for example '<Pitch: C#7 0x10f263e10>'. If the pitch is
    #  empty the string will show '<Pitch: empty 0x10f263b50>'.
    #  See also: string().
    def __str__(self):
        if self.is_empty():
            return '<Pitch: empty>'
        else:
            return f'<Pitch: {self.string()} {hex(id(self))}>'

    ## Prints the external form of the Pitch that, if evaluated
    #  would create a Pitch with the same content as this pitch.
    #  Examples: 'Pitch("C#7")' and Pitch().  See also string().
    def __repr__(self):
        if self.is_empty():
            return 'Pitch()'
        else:
            return f'Pitch("{self.string()}")'



    ## Implements Pitch < Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than the other.
    #
    # This method should call self.pos() and other.pos() to get the
    # two values to compare. See: pos().
    def __lt__(self, other):
        if isinstance(other, Pitch):
            if self.pos() < other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Implements Pitch <= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if isinstance(other, Pitch):
            if self.pos() <= other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Implements Pitch == Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if isinstance(other, Pitch):
            if self.pos() == other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Implements Pitch != Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is not equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if isinstance(other, Pitch):
            if self.pos() != other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Implements Pitch >= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if isinstance(other, Pitch):
            if self.pos() >= other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Implements Pitch > Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater than the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if isinstance(other, Pitch):
            if self.pos() > other.pos():
                return True
            else:
                return False
        else:
            raise ValueError("You cannot compare {} with a Pitch".format(other))

    ## Returns a unique integer representing this pitch's position in
    #  the octave-letter-accidental space. The expression to calculate
    #  this value is (octave<<8) + (letter<<4) + accidental.
    def pos(self):
        return (self.octave << 8) + (self.letter << 4) + self.accidental

    ## Returns true if the Pitch is empty. A pitch is empty if its
    # letter, accidental and octave attributes are None. Only one of
    # these attributes needs to be checked because __init__ will only
    # create a Pitch if all three are legal values or all three are None.
    def is_empty(self):
        if self.letter is None:
            return True
        return False

    ## Returns a string containing the pitch name including the
    #  letter, accidental, and octave.  For example,
    #  Pitch("C#7").string() would return 'C#7'.
    def string(self):
        if self.is_empty():
            return 'empty'
        else:
            if self.octave == -1:
                return f"{Pitch.letterDict[self.letter]}{Pitch.accDict[self.accidental]}00"
            else:
                return f"{Pitch.letterDict[self.letter]}{Pitch.accDict[self.accidental]}{Pitch.octDict[self.octave]}"

    ## Returns the midi key number of the Pitch.
    def keynum(self):
        letterDict = {0: 0,
                      1: 2,
                      2: 4,
                      3: 5,
                      4: 7,
                      5: 9,
                      6: 11, }
        accidentals = {0: -2,
                       1: -1,
                       2: 0,
                       3: 1,
                       4: 2}
        midi = letterDict[self.letter]
        midi = midi + accidentals[self.accidental]
        midi += self.octave * 12
        if midi <= 127 and midi >= 0:
            return midi
        else:
            raise ValueError(f"The pitch is outside the valid midi range of 0-127. Your pitch is midi value {midi}")

    ## Returns the pnum (pitch class enum) of the Pitch. Pnums enumerate
    #  and order the letter and accidental of a Pitch so they can be compared,
    #  e.g.: C < C# < Dbb. See also: pnums.
    def pnum(self):
        accidentals = {0: 'ff',
                       1: 'f',
                       2: '',
                       3: 's',
                       4: 'ss'}
        pitchString = Pitch.letterDict[self.letter]
        pitchString += accidentals[self.accidental]
        return Pitch.pnums[pitchString]


    ## Returns the pitch class (0-11) of the Pitch.
    def pc(self):
        letterDict = {0: 0,
                      1: 2,
                      2: 4,
                      3: 5,
                      4: 7,
                      5: 9,
                      6: 11, }
        accidentals = {0: -2,
                       1: -1,
                       2: 0,
                       3: 1,
                       4: 2}
        pc = letterDict[self.letter] + accidentals[self.accidental]
        return pc % 12

    ## Returns the hertz value of the Pitch.
    def hertz(self):
        return 440.0 * 2 ** ((round(self.keynum()) - 69) / 12)

    ## A @classmethod that creates a Pitch for the specified
    #  midi key number.
    #  @param keynum A valid keynum 0-127.
    #  @param acci  The accidental to use. If no accidental is provided
    #  a default is chosen from C C# D Eb F F# G Ab A Bb B
    #  @returns a new Pitch with an appropriate spelling.
    #
    #  The function should raise a ValueError if the midi key number
    #  is invalid or if the pitch requested does not support the specified
    #  accidental.
    @classmethod
    def from_keynum(cls, keynum, acci=None):
        letterDict = {0: ['C', 'Ebbb', 'Dbb', '', 'C', 'B#', '', 'A###'],
                      1: ['C#', 'Ebb', '', 'Db', '', 'C#', '', 'B##'],
                      2: ['D', 'Fbbb', 'Ebb', '', 'D', '', 'C##', 'B###'],
                      3: ['Eb', '', 'Fbb', 'Eb', '', 'D#', '', 'C###'],
                      4: ['E', '', '', 'Fb', 'E', 'D', 'D##', ''],
                      5: ['F', '', 'Gbb', '', 'F', 'E#', '', 'D###'],
                      6: ['F#', 'Abbb', '', 'Gb', '', 'F#', 'E##', ''],
                      7: ['G', '', 'Abb', '', 'G', '', 'F##', ''],
                      8: ['Ab', 'Bbbb', '', 'Ab', '', 'G#', '', 'F###'],
                      9: ['A', '', 'Bbb', '', 'A', '', 'G##', ''],
                      10: ['Bb','Dbbb', 'Cbb', 'Bb', '', 'A#', 'G###'],
                      11: ['B','Dbbb', '', 'Cb', 'B', '', 'A##', ''],
                      }
        acciDict = {'bbb': 1,
                    'bb': 2,
                    'b': 3,
                    '': 4,
                    '#': 5,
                    '##': 6,
                    '###': 7}
        if keynum <= 127 and keynum >= 0:
            octave, pc = divmod(keynum, 12)
            if acci is None:
                pitchString = letterDict[pc][0] + str(octave - 1)
            else:
                if pc == 0 and acci == '#':
                    octave -= 1
                if (pc == 10 and acci == 'bb') or (pc == 11 and acci == 'b'):
                    octave += 1
                pitchString = letterDict[pc][acciDict[acci]] + str(octave - 1)
            return Pitch(pitchString)
        else:
            raise ValueError("This cannot be a valid pitch")

if __name__ == '__main__':
    print(Pitch.from_keynum(70,'bbb'))
