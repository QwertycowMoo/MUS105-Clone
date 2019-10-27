###############################################################################

from .pitch import Pitch


## A class that implements musical intervals.
#
#  An Interval measures the distance between two Pitches. Interval distance
#  can be measured in different ways, for example using lines-and-spaces,
#  semitones, ratios, or cents. In western music theory an interval distance is
#  measured using 'span' (number of lines and spaces) and 'quality' (a chromatic
#  adjustment to the size). The Interval class supports the standard interval
#  names and classification system, including the notion of descending or
#  ascending intervals and simple or compound intervals.
#  Intervals can be numerically compared for their size (span+quality) and
#  can be used to transpose Pitches.
#
#  An Interval contains four integer attributes:
#  * span  The number of lines and spaces the interval moves (0-7).
#  * qual  The quality of the interval (0-12).
#  * xoct  The 'extra octaves' spanned by compound intervals (0-10).
#  * sign  1 for ascending intervals, -1 for descending.
#
#  See also: https://en.wikipedia.org/wiki/Interval_(music)


class Interval:
    ## Creates an Interval from a string, list, or two Pitches.
    #  * Interval(string) - creates an Interval from a pitch string.
    #  * Interval([s, q, x, s]) - creates a Pitch from a list of four
    #  integers: a span, quality, extra octaves and sign. (see below).
    #  * Interval(pitch1, pitch2) - creates an Interval from two Pitches.
    #
    #  @param arg If only arg is specified it should be either an
    #  interval string or a list of four interval indexes.  If both
    #  arg and other are provided, both should be a Pitch.
    #  @param other A Pitch if arg is a Pitch, otherwise None.
    #
    # The format of a Interval string is:
    #  @code
    #  interval  = ["-"] , <quality> , <span>
    #  <quality> = <diminished> | <minor> | <perfect> | <major> | <augmented>
    #  <diminished> = <5d> , <4d> , <3d> , <2d> , <1d> ;
    #  <5d> = "ooooo" | "ddddd"
    #  <4d> = "oooo" | "dddd"
    #  <3d> = "ooo" | "ddd"
    #  <2d> = "oo" | "dd"
    #  <1d> = "o" | "d"
    #  <minor> = "m"
    #  <perfect> = "P"
    #  <major> = "M"
    #  <augmented> = <5a>, <4a>, <3a>, <2a>, <1a>
    #  <5d> = "+++++" | "aaaaa"
    #  <4d> = "++++" | "aaaa"
    #  <3d> = "+++" | "aaa"
    #  <2d> = "++" | "aa"
    #  <1d> = "+" | "a"
    #  <span> = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ...
    # @endcode
    #
    # The __init__function should check to make sure the arguments are either a string, a
    # list of four integers, or two pitches.  If the input is a string then __init__ should
    # pass the string to the the private _init_from_string() method (see below).  If the
    # input is a list of four ints, __init__ will pass them to the private _init_from_list()
    # method (see below). If the input is two pitches they will be passed to the private
    # _init_from_pitches() method (see below).  Otherwise (if the input is not
    # a string, list of four integers, or two pitches) the method will raise a TypeError
    # for the offending value.

    _5dim_qual, _4dim_qual, _3dim_qual, _2dim_qual, _1dim_qual, _min_qual, _perf_qual, \
    _maj_qual, _1aug_qual, _2aug_qual, _3aug_qual, _4aug_qual, _5aug_qual = range(13)

    _unison_span, _2nd_span, _3rd_span, _4th_span, _5th_span, _6th_span, _7th_span, _octave_span = range(8)
    accidentalSafeDict = {0: "ddddd",
                          1: "dddd",
                          2: "ddd",
                          3: "dd",
                          4: "d",
                          5: "m",
                          6: "P",
                          7: "M",
                          8: "A",
                          9: "AA",
                          10: "AAA",
                          11: "AAAA",
                          12: "AAAAA"
                          }

    accidentalDict = {0: "ooooo",
                      1: "oooo",
                      2: "ooo",
                      3: "oo",
                      4: "o",
                      5: "m",
                      6: "P",
                      7: "M",
                      8: "+",
                      9: "++",
                      10: "+++",
                      11: "++++",
                      12: "+++++"
                      }

    acciStrDict = {12: 'quintuply-augmented',
                   11: 'quadruply-augmented',
                   10: 'triply-augmented',
                   9: 'doubly-augmented',
                   8: 'augmented',
                   7: 'major',
                   6: 'perfect',
                   5: 'minor',
                   4: 'diminished',
                   3: 'doubly-diminished',
                   2: 'triply-diminished',
                   1: 'quadruply-diminished',
                   0: 'quintuply-diminished'}
    intervalStrDict = {0: 'unison',
                       1: 'second',
                       2: 'third',
                       3: 'fourth',
                       4: 'fifth',
                       5: 'sixth',
                       6: 'seventh',
                       7: 'octave'}

    invert_acci_dict = dict([[v, k] for k, v in accidentalDict.items()])
    invert_accisafe_dict = dict([[v, k] for k, v in accidentalSafeDict.items()])

    majorminor = [1, 2, 5, 6]
    perfect = [0, 3, 4, 7]

    diatonicDict = {0: 0,
                    1: 2,
                    2: 4,
                    3: 5,
                    4: 7,
                    5: 9,
                    6: 11,
                    7: 12}

    majMinAdj = {_4dim_qual: -5,
                 _3dim_qual: -4,
                 _2dim_qual: -3,
                 _1dim_qual: -2,
                 _min_qual: -1,
                 _maj_qual: 0,
                 _1aug_qual: 1,
                 _2aug_qual: 2,
                 _3aug_qual: 3,
                 _4aug_qual: 4}
    perfAdj = {_5dim_qual: -5,
               _4dim_qual: -4,
               _3dim_qual: -3,
               _2dim_qual: -2,
               _1dim_qual: -1,
               _perf_qual: 0,
               _1aug_qual: 1,
               _2aug_qual: 2,
               _3aug_qual: 3,
               _4aug_qual: 4,
               _5aug_qual: 5}

    def __init__(self, arg, other=None):

        if isinstance(arg, list):
            if len(arg) != 4:
                raise ValueError("This is not a valid list to create an interval")
            else:
                interval = self._init_from_list(arg[0], arg[1], arg[2], arg[3])
                self.span = interval[0]
                self.qual = interval[1]
                self.xoct = interval[2]
                self.sign = interval[3]

        elif isinstance(arg, str):
            interval = self._init_from_string(arg)
            self.span = interval[0]
            self.qual = interval[1]
            self.xoct = interval[2]
            self.sign = interval[3]
        elif isinstance(other, Pitch) and isinstance(arg, Pitch):
            interval = self._init_from_pitches(arg, other)
            self.span = interval[0]
            self.qual = interval[1]
            self.xoct = interval[2]
            self.sign = interval[3]
        else:
            raise ValueError("This is not a valid interval")

    ## A private method that checks four integer values (span, qual, xoct, sign) to make sure
    # they are valid index values for the span, qual, xoct and sign attributes. Legal values
    # are: span 0-7, qual 0-12, xoct 0-10, sign -1 or 1. If any value is out of range the
    # method will raise a ValueError for that value. If all values are legal the method will
    # make the following 'edge case' tests:
    # * span and quality values cannot produce negative semitones, i.e. an interval
    #   whose 'top' would be lower that its 'bottom'. Here are the smallest VALID 
    #   interval for each span that could cause this: perfect unison, diminished-second,
    #   triply-diminished third.
    # * Only the span of a fifth can be quintuply diminished.
    # * Only the span of a fourth can be quintuply augmented.
    # * No interval can surpass 127 semitones. The last legal intervals are: 'P75'
    #  (a 10 octave perfect 5th), and a 'o76' (a 10 octave diminished 6th) 
    # * If a user specifies an octave as a unison span with 1 extra octave, e.g. [0,*,1,*],
    # it should be converted to an octave span with 0 extra octaves, e.g. [7,*,0,*]
    #
    # Only if all the edge case checks pass then _init_from_list() should assign
    # the four values to the attributes, e.g. self.span=span, self.qual=qual, and
    # so on. Otherwise if any edge case fails the method should raise a ValueError.
    def _init_from_list(self, span, qual, xoct, sign):

        if span >= 0 and span < 9:
            if (Interval.accidentalDict.get(qual, "none") != "none"):

                # check for valid minor/Perfect/Major
                for interval in Interval.majorminor:
                    if span == interval:
                        if qual == 6:
                            raise ValueError(f"A span of {self.span} cannot be a Perfect interval")
                        break
                # already checked if it is a major or a minor
                # we can assume that is a perfect interval because it already passed the span tests
                # but need to not check this if we already have something

                for interval in Interval.perfect:
                    if span == interval:
                        if qual == Interval._maj_qual or qual == Interval._min_qual:
                            raise ValueError(f"A span of {self.span} cannot be a major or minor interval")
                        if qual == Interval._5dim_qual and not span == Interval._5th_span:
                            raise ValueError("Only a fifth can be quintuply diminished")
                        if qual == Interval._5aug_qual and not span == Interval._4th_span:
                            raise ValueError("Only a fourth can be quintuply augmented")
                        break
                if xoct >= 0 and xoct <= 10:
                    # checking for octave perfect unison
                    if span == Interval._unison_span and xoct > 0:
                        span = Interval._octave_span
                        xoct -= 1

                    # checking for outside the 127 range
                    if xoct == 10 and span > Interval._7th_span:
                        raise ValueError("This interval is outside the range of 127 semitones")
                    elif xoct == 10 and span == Interval._7th_span and qual > Interval._1dim_qual:
                        raise ValueError("This interval is outside the range of 127 semitones")
                    elif xoct == 10 and span == Interval._6th_span and qual > Interval._perf_qual:
                        raise ValueError("This interval is outside the range of 127 semitones")
                    elif xoct == 10 and span == Interval._5th_span and qual > Interval._2aug_qual:
                        raise ValueError("This interval is outside the range of 127 semitones")
                    if not sign == 1 or not sign == -1:
                        if sign == 1:
                            if span == Interval._unison_span and qual < Interval._perf_qual \
                                    or span == Interval._2nd_span and qual < Interval._1dim_qual \
                                    or span == Interval._3rd_span and qual < Interval._3dim_qual:
                                if xoct == 0:
                                    raise ValueError("An ascending interval cannot have a negative number of semitones")
                    else:
                        raise ValueError("This is not a valid direction for the interval")
                else:
                    raise ValueError("This is not a valid amount of extra octave(s)")
            else:
                raise ValueError("This is not a valid quality")
        else:
            raise ValueError("This is not a valid span")

        return (span, qual, xoct, sign)

    ## A private method that accepts an interval string and parses it into four
    # integer values: span, qual, xoct, sign. If all four values can be parsed
    # from the string they should be passed to the _init_from_list() method to
    # check the values and assign them to the instance's attributes. A ValueError
    # should be raised for any value that cannot be parsed from the string. See:
    # _init_from_list().
    def _init_from_string(self, string):
        # ... parse the string into a span, qual, xoct and sign values
        span, qual, xoct, sign = (-1, -1, -1, -1)
        # ... pass on to check an assign instance attributes.

        intervalChar = list(string)
        counter = 1
        num = intervalChar[len(intervalChar) - counter]

        while num.isnumeric():
            counter += 1
            num = intervalChar[len(intervalChar) - counter]
        counter -= 1
        num = int(''.join(intervalChar[len(intervalChar) - counter:]))

        intervalChar = intervalChar[:len(intervalChar) - counter]
        print(intervalChar)
        xoct, span = divmod(num, 8)
        if xoct == 0:
            span -= 1
        if num == "0":
            if intervalChar[len(intervalChar) - 2] == "1":
                num = 10
                intervalChar.pop(len(intervalChar) - 2)
        if intervalChar[0] == '-':
            sign = -1
            intervalChar.pop(0)
        else:
            sign = 1

        qual = Interval.invert_acci_dict.get("".join(intervalChar), "none")
        if qual == "none":
            qual = Interval.invert_accisafe_dict.get("".join(intervalChar), "none")
        print(span, qual, xoct, sign)
        return self._init_from_list(span, qual, xoct, sign)

    ## A private method that determines approprite span, qual, xoct, sign
    # from two pitches. If pitch2 is lower than pitch1 then a descending
    # interval should be formed. The values should be passed to the
    # _init_from_list() method to initalize the interval's attributes.
    # See: _init_from_list().
    #
    # Do NOT implement this method yet.
    def _init_from_pitches(self, pitch1, pitch2):

        diatonicDict = {0: 0,
                        1: 2,
                        2: 4,
                        3: 5,
                        4: 7,
                        5: 9,
                        6: 11,
                        7: 12}

        majMinAdj = {-5: Interval._4dim_qual,
                     -4: Interval._3dim_qual,
                     -3: Interval._2dim_qual,
                     -2: Interval._1dim_qual,
                     -1: Interval._min_qual,
                     0: Interval._maj_qual,
                     1: Interval._1aug_qual,
                     2: Interval._2aug_qual,
                     3: Interval._3aug_qual,
                     4: Interval._4aug_qual}
        perfAdj = {-5: Interval._5dim_qual,
                   -4: Interval._4dim_qual,
                   -3: Interval._3dim_qual,
                   -2: Interval._2dim_qual,
                   -1: Interval._1dim_qual,
                   0: Interval._perf_qual,
                   1: Interval._1aug_qual,
                   2: Interval._2aug_qual,
                   3: Interval._3aug_qual,
                   4: Interval._4aug_qual,
                   5: Interval._5aug_qual}

        # ... parse the string into a span, qual, xoct and sign values
        span, qual, xoct, sign = (-1, -1, -1, -1)

        if (pitch1 < pitch2):

            sign = 1
        else:
            sign = -1
            temp = pitch1
            pitch1 = pitch2
            pitch2 = temp

        span = pitch2.letter - pitch1.letter
        while span < 0:
            span += Interval._octave_span
        semitones = pitch2.keynum() - pitch1.keynum()
        diaSeparation = diatonicDict.get(pitch2.letter) - diatonicDict.get(pitch1.letter)
        while diaSeparation < 0:
            diaSeparation += 12
        print("span:" + str(span), "semitones: " + str(semitones), "diatonic separation:" + str(diaSeparation))
        if semitones - diaSeparation < 0:
            xoct, qual = divmod(semitones - diaSeparation, -12)
        else:
            xoct, qual = divmod(semitones - diaSeparation, 12)
        print("xtraOct: " + str(xoct), "qual: " + str(qual))
        if span in Interval.majorminor:
            if pitch1.letter == 2 or pitch1.letter == 6:
                qual -= 1
            qual = majMinAdj.get(qual)
        else:
            if pitch1.letter == 3 and pitch2.letter == 6:
                qual += 1
            elif pitch1.letter == 6 and pitch2.letter != 2:
                qual -= 1
            qual = perfAdj.get(qual)
        # find direction first. Then whether the letter is higher in the index than the other
        # complement of an interval is 8va - (L1 - L2), regular span is L2 - L1
        print(span, qual, xoct, sign)
        # needs to fix complement and octaves and such
        # ... pass on to check and assign instance attributes.
        return self._init_from_list(span, qual, xoct, sign)

    ## Returns a string displaying information about the
    #  Interval within angle brackets. Information includes the
    #  the class name, the interval text, the span, qual, xoct and sign
    #  values, and the id of the object. Example:
    #  <Interval: oooo8 [7, 1, 0, 1] 0x1075bf6d0>
    #  See also: string().
    def __str__(self):
        return f'<Interval: {self.string()} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'

    ## The string the console prints shows the external form.
    # Example: Interval("oooo8")
    def __repr__(self):
        return f'Interval("{self.string()}")'

    ## Implements Interval < Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __lt__(self, other):
        if isinstance(other, Interval):
            print(other.pos(), self.pos())
            if other.pos() > self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Implements Interval <= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is less than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __le__(self, other):
        if isinstance(other, Interval):
            if other.pos() >= self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Implements Interval == Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __eq__(self, other):
        if isinstance(other, Interval):
            if other.pos() == self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Implements Interval != Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is not equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ne__(self, other):
        if isinstance(other, Interval):
            if other.pos() != self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Implements Interval >= Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than or equal to the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __ge__(self, other):
        if isinstance(other, Interval):
            if other.pos() <= self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Implements Interval > Interval.
    # @param other The interval to compare with this interval.
    # @returns True if this interval is greater than the other.
    #
    # A TypeError should be raised if other is not an Interval.
    # This method should call self.pos() and other.pos() to get the
    # values to compare. See: pos().
    def __gt__(self, other):
        if isinstance(other, Interval):
            if other.pos() < self.pos():
                return True
            else:
                return False
        else:
            raise TypeError("What is being compared is not an Interval")

    ## Returns a numerical value for comparing the size of this interval to
    # another. The comparison depends on the span, extra octaves, and quality
    # of the intervals but not their signs. For two intervals, if the span of
    # the first (including extra octaves) is larger than the second then the
    # first interval is larger than the second regardless of the quality of
    # either interval. If the interval spans are the same then the first is
    # larger than the second if its quality is larger. This value can be
    # encoded as a 16 bit integer: (((span + (xoct * 7)) + 1) << 8) + qual  
    def pos(self):
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual

    ## Returns a string containing the interval name.
    #  For example, Interval('-P5').string() would return '-P5'.
    def string(self):
        intString = ""
        if self.sign == -1:
            intString = "-"
        return intString + str(Interval.accidentalDict[self.qual]) + str(self.span + 1 + self.xoct * 7)

    ## Returns the full interval name, e.g. 'doubly-augmented third'
    #  or 'descending augmented sixth'
    # @param sign If true then "descending" will appear in the
    # name if it is a descending interval.
    def full_name(self, *, sign=True):

        returnStr = ""
        if sign == True:
            if self.sign == -1:
                returnStr += "descending "
            returnStr += self.span_name() + " "
            returnStr += self.quality_name()
        return returnStr

    ## Returns the full name of the interval's span, e.g. a
    # unison would return "unison" and so on.
    def span_name(self):
        return Interval.intervalStrDict.get(self.span, "none")

    ## Returns the full name of the interval's quality, e.g. a
    # perfect unison would return "perfect" and so on.
    def quality_name(self):
        return Interval.acciStrDict.get(self.qual, "none")

    ## Returns true if this interval and the other interval have the
    # same span, quality and sign. The extra octaves are ignored.
    def matches(self, other):
        if isinstance(other, Interval):
            if self.sign == other.sign:
                if self.qual == other.qual:
                    if self.span == other.span:
                        return True
            return False
        else:
            raise ValueError(f"You cannot compare {other} to an interval!")

    ## Returns the interval's number of lines and spaces, e.g.
    # a unison will return 1.
    def lines_and_spaces(self):
        if self.span == 0:
            return 1
        return self.span + 1

    ## Private method that returns a zero based interval quality from its 
    #  external name. Raises an assertion if the name is invalid. See:
    # is_unison() and similar.
    def _to_iq(self, name):
        pass

    ## Returns the interval values as a list: [span, qual, xoct, sign]
    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]

    ## Returns true if the interval is a unison otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of unison, which can be any valid quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_unison(self, qual=None):
        if self.span == Interval._unison_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a second otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of second, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_second(self, qual=None):
        if self.span == Interval._2nd_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a third otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of third, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_third(self, qual=None):
        if self.span == Interval._3rd_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a fourth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fourth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fourth(self, qual=None):
        if self.span == Interval._4th_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a fifth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of fifth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_fifth(self, qual=None):
        if self.span == Interval._5th_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a sixth otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of sixth, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_sixth(self, qual=None):
        if self.span == Interval._6th_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is a seventh otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of seventh, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_seventh(self, qual=None):
        if self.span == Interval._7th_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns true if the interval is an octave otherwise false.
    # @param qual If specified the predicate tests for that specific
    # quality of octave, which can be any quality symbol, e.g.
    # 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
    def is_octave(self, qual=None):
        if self.span == Interval._octave_span:
            if qual == None:
                return True
            else:
                if isinstance(qual, str):
                    if Interval.invert_acci_dict.get(qual, "none") == self.qual:
                        return True
                    else:
                        if Interval.invert_accisafe_dict.get(qual, "none") == self.qual:
                            return True
                        return False
                else:
                    raise ValueError('This is not a valid quality')

    ## Returns a 'diminution count' 1-5 if the interval is diminished else False.
    # For example, if the interval is doubly-diminished then 2 is returned.
    # If the interval not diminished at all (e.g. is perfect, augmented, minor or
    # major) then False is returned.
    def is_diminished(self):
        if self.qual > 4:
            return False
        else:
            return self.qual + 1

    ## Returns true if the interval is minor, otherwise false.
    def is_minor(self):
        if self.qual == 5:
            return True
        else:
            return False

    ## Returns true if the interval is perfect, otherwise false.
    def is_perfect(self):
        if self.qual == 6:
            return True
        else:
            return False

    ## Returns true if the interval is major, otherwise false.
    def is_major(self):
        if self.qual == 7:
            return True
        else:
            return False

    ## Returns a 'augmentation count' 1-5 if the interval is augmented else False.
    # For example, if the interval is doubly-augmented then 2 is returned.
    # If the interval not augmented at all (e.g. is perfect, diminished, minor or
    # major) then False is returned.
    def is_augmented(self):
        if self.qual < 8:
            return False
        else:
            return 6 - (13 - self.qual)

    ## Returns true if the interval belongs to the 'perfect interval'
    #  family, i.e. it is a Unison, 4th, 5th, or Octave.
    def is_perfect_type(self):
        if self.span in Interval.perfect:
            return True
        else:
            return False

    ## Returns true if this interval belongs to the 'imperfect interval'
    #  family, i.e. it is a 2nd, 3rd, 6th, or 7th.
    def is_imperfect_type(self):
        if self.span in Interval.majorminor:
            return True
        else:
            return False

    ## Returns true if this is a simple interval, i.e. its span is
    #  less-than-or-equal to an octave.
    def is_simple(self):
        if self.xoct == 0:
            return True
        else:
            return False

    ## Returns true if this is a compound interval, i.e. its span is
    #  more than an octave (an octave is a simple interval).
    def is_compound(self):
        if self.xoct > 0:
            return True
        else:
            return False

    ## Returns true if this interval's sign is 1.
    def is_ascending(self):
        if self.sign == 1:
            return True
        else:
            return False

    ## Returns true if this interval's sign is -1.
    def is_descending(self):
        if self.sign == -1:
            return True
        else:
            return False

    ## Returns true if the interval is a consonant interval. In this
    # context the perfect fourth should be considered consonant.
    def is_consonant(self):
        if self.is_imperfect_type():
            if self.is_major() or self.is_minor():
                return True
            else:
                return False
        else:
            if self.is_perfect():
                return True
            else:
                return False

    ## Returns true if the interval is not a consonant interval.
    def is_dissonant(self):
        if self.is_augmented() or self.is_diminished():
            return True
        else:
            return False

    ##  Returns a complemented copy of the interval. To complement an interval
    # you invert its span and quality. To invert the span, subtract it from
    # the maximum span index (the octave index). To invert the  quality subtract
    # it from the maximum quality index (quintuply augmented).
    def complemented(self):
        return Interval([Interval._octave_span - self.span, Interval._5aug_qual - self.qual, self.xoct, self.sign])

    ## Returns the number of semitones in the interval. It is possible
    # to determine the number of semitones by looking at the span and
    # quality indexes. For example, if the span is a perfect fifth
    # (span index 4) and the quality is perfect (quality index 6)
    # then the semitones will be 5 and augmented or diminished fifths
    # will add or subtract semitones accordingly.
    #
    # This value will be negative for descending intervals otherwise positive.
    def semitones(self):
        semitones = Interval.diatonicDict.get(self.span)
        if self.xoct > 0:
             semitones = semitones + (12 * self.xoct)
        if self.span in Interval.majorminor:
            semitones += Interval.majMinAdj.get(self.qual)
        else:
            semitones += Interval.perfAdj.get(self.qual)
        return semitones

    ## Adds a specified interval to this interval.
    #  @return  a new interval expressing the total span of both intervals.
    #  @param other the interval to add to this one.
    #
    # A TypeError should be raised if other is not an interval. A
    # NotImplementedError if either intervals are descending.
    def add(self, other):
        if isinstance(other, Interval):
            span = ((self.span + other.span) - 1) % 7
            # still need to finish

    # Transposes a Pitch or Pnum by the interval. Pnum transposition
    #  has no direction so if the interval is negative its complement
    #  should be used.
    #  @param pref  The Pitch or Pnum to transpose.
    #  @return The transposed Pitch or Pnum.
    def transpose(self, pref):
        #still need handle pnum cases
        if isinstance(pref, Pitch):
            if self.sign == -1:
                if self.span > pref.letter:
                    pref.octave -= 1
                pref.letter = (pref.letter + 7 - self.span) % 7
                if self.is_major() or self.is_minor():
                    pref.accidental -= Interval.majMinAdj.get(self.qual)
                else:
                    pref.accidental -= Interval.perfAdj.get(self.qual)
            else:
                pref.letter = pref.letter + self.span % 7
                if self.is_major() or self.is_minor():
                    pref.accidental += Interval.majMinAdj.get(self.qual)
                else:
                    pref.accidental += Interval.perfAdj.get(self.qual)
            return Pitch(pref.string())

