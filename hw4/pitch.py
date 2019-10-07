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
    pnums = IntEnum('Pnum', [])

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
        pass
        ## A letter index 0-6.
        # self.letter = None
        ## An accidental index 0-4.
        # self.accidental = None
        ## An octave index 0-10.
        # self.octave = None

    ## Returns a string displaying information about the
    #  pitch within angle brackets. Information includes the
    #  the class name, the pitch text, and the id of the object,
    #  for example '<Pitch: C#7 0x10f263e10>'. If the pitch is
    #  empty the string will show '<Pitch: empty 0x10f263b50>'.
    #  See also: string().
    def __str__(self):
        return ''

    ## Prints the external form of the Pitch that, if evaluated
    #  would create a Pitch with the same content as this pitch.
    #  Examples: 'Pitch("C#7")' and Pitch().  See also string().
    def __repr__(self):
        return ''

    ## Implements Pitch < Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than the other.
    #
    # This method should call self.pos() and other.pos() to get the
    # two values to compare. See: pos().
    def __lt__(self, other):
        pass

    ## Implements Pitch <= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is less than or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        pass

    ## Implements Pitch == Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        pass

    ## Implements Pitch != Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is not equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        pass

    ## Implements Pitch >= Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater or equal to the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        pass

    ## Implements Pitch > Pitch.
    # @param other The pitch to compare with this pitch.
    # @returns True if this Pitch is greater than the other.
    #
    # A TypeError should be raised if other is not a Pitch.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        pass

    ## Returns a unique integer representing this pitch's position in
    #  the octave-letter-accidental space. The expression to calculate
    #  this value is (octave<<8) + (letter<<4) + accidental.
    def pos(self):
        pass

    ## Returns true if the Pitch is empty. A pitch is empty if its
    # letter, accidental and octave attributes are None. Only one of
    # these attributes needs to be checked because __init__ will only
    # create a Pitch if all three are legal values or all three are None.
    def is_empty(self):
        pass

    ## Returns a string containing the pitch name including the
    #  letter, accidental, and octave.  For example,
    #  Pitch("C#7").string() would return 'C#7'.
    def string(self):
        pass

    ## Returns the midi key number of the Pitch.
    def keynum(self):
        pass

    ## Returns the pnum (pitch class enum) of the Pitch. Pnums enumerate
    #  and order the letter and accidental of a Pitch so they can be compared,
    #  e.g.: C < C# < Dbb. See also: pnums.
    def pnum(self):
        pass

    ## Returns the pitch class (0-11) of the Pitch.
    def pc(self):
        pass

    ## Returns the hertz value of the Pitch.
    def hertz(self):
        pass

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
        pass

