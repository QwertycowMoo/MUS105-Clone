###############################################################################

from .ratio import Ratio


## A class representing the standard musical meters.
# See: https://en.wikipedia.org/wiki/Metre_(music)
class Meter:
    ## Constructor.
    # @param num  The numerator, an integer between 1 and 16 inclusive.
    # @param den  The denominator, a power of 2 between 1 and 32 inclusive.
    # @returns A meter instance with attributes num and den.
    #
    # The constructor should raise a TypeError if num or den are not
    # integers and a ValueError if their values are invalid.
    def __init__(self, num, den):
        if (isinstance(num, int)):
            if (isinstance(den, int)):
                if num >= 1 and num <= 16:
                    if den % 2 == 0 and den <= 32:
                        self.num = num
                        self.den = den
                    elif den == 1:
                        self.num = num
                        self.den = den
                    else:
                        raise ValueError("The denominator is not valid")
                else:
                    raise ValueError("The numerator is not valid")
            else:
                raise ValueError("The denominator must be an integer")
        else:
            raise ValueError("The numerator must be an integer")

    ## Returns the print representation of the meter. The string should
    # include the class name, the num and den, and instance id.
    #
    # Examples:
    # <Meter: 2/4 0x1051a1690>
    # <Meter: 7/16 0x1051a1bd0>
    # <Meter: 3/1 0x1053ee910>
    def __str__(self):
        return f'<Meter: {self.string()} {hex(id(self))}>'

    ## Returns the external representation of the meter. The string
    # should include the class name, num and den.
    #
    # Examples:
    # Meter(2, 4)
    # Meter(7, 16)
    # Meter(3, 1)
    def __repr__(self):
        return f'Meter({self.num}, {self.den})'

    ## Returns the string name of the meter, e.g. '6/8'
    def string(self):
        return f"{self.num}/{self.den}"

    ## Returns true if the meter is compound (numerator 6, 9, 12, or 15).
    def is_compound(self):
        if self.num in [6, 9, 12, 15]:
            return True
        else:
            return False

    ## Returns true if the meter is simple (numerator 1, 2, 3, or 4).
    def is_simple(self):
        if self.num in [1, 2, 3, 4]:
            return True
        else:
            return False

    ## Returns true if the meter is complex (numerator 5, 7, 8, 10, 13, or 14).
    def is_complex(self):
        if self.num in [5, 7, 8, 10, 13, 14]:
            return True
        else:
            return False

    ## Returns true if the meter is duple (numerator 2 or 6).
    def is_duple(self):
        if self.num in [2, 6]:
            return True
        else:
            return False

    ## Returns true if the meter is triple (numerator 3 or 9).
    def is_triple(self):
        if self.num in [3, 9]:
            return True
        else:
            return False

    ## Returns true if the meter is quadruple (numerator 4 or 12).
    def is_quadruple(self):
        if self.num in [4, 12]:
            return True
        else:
            return False

    ## Returns true if the meter is quintuple (numerator 5 or 15).
    def is_quintuple(self):
        if self.num in [5, 15]:
            return True
        else:
            return False

    ## Returns true if the meter is a septuple (numerator 7).
    def is_septuple(self):
        if self.num == 7:
            return True
        else:
            return False

    ## Returns a Ratio representing the meter's beat. For example,
    # 4/4 returns a beat of 1/4, 6/8 meter returns the beat 3/8,
    # and 3/2 returns a beat of 1/2. The method should raise
    # a NotImplementedError If the meter is not simple or compound.
    # See: Ratio.
    def beat(self):
        if self.is_compound() or self.is_simple():
            if self.is_duple():
                return Ratio(int(self.num / 2), self.den)
            if self.is_triple():
                return Ratio(int(self.num / 3), self.den)
            if self.is_quadruple():
                return Ratio(int(self.num / 4), self.den)
            if self.is_quintuple():
                return Ratio(int(self.num / 5), self.den)
            if self.is_septuple():
                return Ratio(int(self.num / 7), self.den)
            else:
                return Ratio(self.num, self.den)
        else:
            raise NotImplementedError("Nope")

    ## Returns a Ratio representing the meter's total measure duration, in beats.
    # For example, 4/4 returns a duration ratio of 1/1, 6/8 meter returns 3/4,
    # and 3/2 returns a duration of 3/2. See: Ratio.
    def measure_dur(self):
        return Ratio(self.num, self.den)
