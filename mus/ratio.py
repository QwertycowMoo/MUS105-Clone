
###############################################################################
## @file
#  A class that implements fractional numbers.
#  The Ratio class provides exact arithmetic for representing exact musical
#  quantities such as proportional (metric) time, duration, and 'just' tuning
#  intervals. Ratios can be created from two integers or from a string.
#  Ratios are compared and combined using the standard math operators.

import math


class Ratio:

    ## Creates a Ratio from integers, a floating point number, or a string name.
    #  * Ratio(int, int) - creates a ratio from an integer numerator and denominator.
    #  * Ratio(int) - creates a ratio from an integer numerator with the denominator
    #  set to 1.
    #  * Ratio(float) - creates a ratio from a floating point number
    #  (see: as_integer_ratio())
    #  * Ratio(string) -  creates a ratio from a string 'num/den'. Both num and
    #  den must produce valid integers.
    #
    #  @param num If only num is specified it must be either an integer, float,
    #  or a string containing a valid ratio expression 'a/b'. If both num and
    #  den are provided they must both be integer value.
    #  @param den If specified den must be a non-zero integer denominator
    #
    #  Upon construction the new ratio will always be expressed in its most simple
    #  form, for example Ratio(6,12) will become Ratio(1/2), See: gcd().
    #  If both the numerator and denominator are negative the ratio should be
    #  converted to positive by the constructor.
    #
    #  The constructor should raise a TypeError if the num or den is not a integer,
    #  string or float and a DivisionByZero error if the denominator is 0.
    def __init__(self, num, den=None):

        if den == None:
            if isinstance(num, str):

                strRatio = num.split("/")
                print(strRatio)
                try:
                    self.num = int(strRatio[0])
                    self.den = int(strRatio[1])
                    if self.num < 0 and self.den < 0:
                        self.num = -int(strRatio[0])
                        self.den = -int(strRatio[1])
                except ValueError:
                    raise ValueError("The Ratio is not a valid ratio")
            if isinstance(num, float):
                tupRatio = num.as_integer_ratio()
                self.num = tupRatio[0]
                self.den = tupRatio[1]
            if isinstance(num, int):
                self.num = num
                self.den = 1
        else:
            if isinstance(num, int) and isinstance(den, int):
                self.num = num // math.gcd(num, den)
                self.den = den // math.gcd(num, den)
            else:
                raise ValueError("The Ratio does not have valid inputs. Your inputs were {} and {}".format(num, den))


    ## Returns a string showing the ratio's fraction and the hex
    #  hex value of the ratio's memory address.
    #  Example: <Ratio: 1/4 0x10610d2b0>
    def __str__(self):
        return "<Ratio: {}/{} {}>".format(self.num, self.den, hex(id(self)))

    ## Returns a string expression that will evaluate to this ratio.
    def __repr__(self):
        return "Ratio({},{})".format(self.num, self.den)

    ## Implements Ratio*Ratio, Ratio*int and Ratio*float.
    # @param other An Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __mul__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.num * other.num, self.den * other.den)
        if isinstance(other, int):
            return Ratio(self.num * other, self.den)
        if isinstance(other, float):
            return other * self.num / self.den
        else:
            raise TypeError("You can only multiply by a Ratio, integer, or float")

    ## Implements right side multiplication by calling __mul__
    #__rmul__ = __mul__

    ## Implements Ratio/Ratio, Ratio/int and Ratio/float.
    # @param other A Ratio, int or float.
    # @returns A Ratio if other is a Ratio or an int, otherwise a float.
    #
    # A TypeError should be raised if other is not a Ratio, int or float.
    def __truediv__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.num * other.den, self.den * other.num)
        if isinstance(other, int):
            return Ratio(self.num / other, self.den)
        if isinstance(other, float):
            return (self.num / other) / self.den
        else:
            raise TypeError("You can only multiply by a Ratio, integer, or float")

    ## Implements int / Ratio or float / Ratio (right side division).
    #  @returns A new Ratio.
    def __rtruediv__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.den * other.num, self.num * other.den)
        if isinstance(other, int):
            return other / self.num * self.den
        if isinstance(other, float):
            return other / self.num * self.den
        else:
            raise TypeError("You cannot divide {} by a Ratio".format(other))

    ## Implements 1 / ratio (reciprocal).
    #  @returns A new Ratio.
    def __invert__(self):
        return Ratio(self.den, self.num)

    ## Implements Ratio + Ratio, Ratio + int and Ratio + float. In order to
    #  add two ratios their denominators must be converted to the
    #  least common multiple of the current denominator. See: lcm().
    #  @returns A new Ratio.
    def __add__(self, other):
        if isinstance(other, Ratio):
            return Ratio((self.num * other.den) + (other.num * self.den), self.den * other.den)
        if isinstance(other, int):
            return Ratio(self.num + (other * self.den), self.den)
        if isinstance(other, float):
            return Ratio((self.num / self.den) + other)
        else:
            raise TypeError("You cannot add {} with a Ratio".format(other))


    ## Implements right side addition by calling __add__.
    #  @returns A new Ratio.
    #__radd__ = __add__

    ## Implements -ratio (negation).
    #  @returns A new Ratio.
    def __neg__(self):
        return Ratio(-self.num, self.den)

    ## Implements ratio - ratio, ratio - int and ratio - float.
    #  @returns A new Ratio.
    def __sub__(self, other):
        if isinstance(other, Ratio):
            return self.__add__(other.__neg__())
        if isinstance(other, int):
            return self.__add__(other.__neg__())
        if isinstance(other, float):
            return self.__add__(other.__neg__())
        else:
            raise TypeError("You cannot subtract a Ratio with your input, {}".format(other))



    ## Implements int - ratio and float-ratio (right side subtraction).
    #  @returns A new Ratio.
    def __rsub__(self, other):
        # other is the LEFT side non-ratio operand.

        if isinstance(other, int):
            return Ratio((other * self.den) - self.num, self.den)
        if isinstance(other, float):
            return Ratio(other.as_integer_ratio()[0], other.as_integer_ratio()[1]).__add__(self.__neg__())
        else:
            raise TypeError("You cannot subtract a Ratio with your input, {}".format(other))

    ## Implements ratio % ratio.
    #  @returns A new Ratio.
    def __mod__(self, other):
        if isinstance(other, Ratio) or isinstance(other, int) or isinstance(other, float):
            modRatio = Ratio(self.num, self.den)
            while modRatio.num > 0:
                modRatio = modRatio.__sub__(other)
            if modRatio.num == 0:
                return modRatio
            else:
                return modRatio.__add__(other)
        else:
            raise TypeError("You cannot use modulo with your input {}".format(other))



    ## Implements Ratio**int, Ratio**float, and Ratio**Ratio.
    #  @returns If the exponent is a positive or negative int
    #  a Ratio should be returned. Otherwise for Ratio or float
    #  exponents a float should be returned. See: math.pow().
    def __pow__(self, other):
        if isinstance(other, int):
            expRatio = Ratio(self.num, self.den)
            if other > 0:
                for i in range(other - 1):
                    expRatio *= self
                return expRatio
            elif other < 0:
                for i in range(abs(other) - 1):
                    expRatio /= self
                return expRatio
            elif other == 0:
                return Ratio(1,1)
        elif isinstance(other, Ratio) or isinstance(other, float):
            return math.pow(self.num / self.den, other)
        else:
            raise ValueError("You cannot raise a Ratio by {}".format(other))
    ## Implements an int**ratio or float**ratio
    #  @param other  The base integer or float.
    #  @returns A floating point number.
    #
    #  The function can be implemented using math.pow().
    def __rpow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return math.pow(other, self.num/self.den)
        else:
            raise ValueError("You cannot raise {} by a Ratio".format(other))
    ## Implements Ratio < Ratio, Ratio < int, Ratio < float. See: compare().
    def __lt__(self, other):
        pass

    ## Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __le__(self, other):
        pass

    ## Implements Ratio <= Ratio, Ratio <= int, Ratio <= float. See: compare().
    def __eq__(self, other):
        pass

    ## Implements Ratio != Ratio, Ratio != int, Ratio != float. See: compare().
    def __ne__(self, other):
        pass

    ## Implements Ratio >= Ratio, Ratio >= int, Ratio >= float. See: compare().
    def __ge__(self, other):
        pass

    ## Implements Ratio>Ratio, Ratio > int, Ratio > float. See: compare().
    def __gt__(self, other):
        pass

    ## Returns a single integer hash value for the ratio: (num<<16 + den)
    def __hash__(self):
        pass

    ## Helper method implements ratio comparison. Returns 0 if the ratios are equal,
    # a negative value if self is less than other and a positive value if self is
    # GEQ other. Given two ratios the comparison is (num1*den2) - (num2/den1)
    def compare(self, other):
        if isinstance(other, Ratio):
            #basically only taking the top part of the fraction comparison
            return (self.num * other.den) - (other.num * self.den)
        else:
            raise ValueError("What is being compared to is not a Ratio!")

    ## A static method that returns the lowest common multiple of two integers
    # a and b. lcm be calculated using gcd(): (a*b) // gcd(a,b)
    @staticmethod
    def lcm(a, b):
        return (a*b) // math.gcd(a,b)



    ## Returns the string name of the ratio 'num/den'.
    def string(self):
        pass

    ## Returns 1/ratio.
    def reciprocal(self):
        return Ratio(self.den, self.num)

    ## Returns the musical 'dotted' value of the ratio, e.g. 1/4 with
    #  one dot is 1/4 + 1/8 = 3/8.
    #  @param dots  The number of dots to apply, each dot adds half the
    #  previous value of the ratio.
    #  @return A new ratio representing the dotted value.

    # The method should raise a ValueError if dots is not a positive integer.
    def dotted(self, dots=1):
        pass

    ## Returns a list of num sub-divisions (metric 'tuples') that sum to
    #  value of ratio*num.
    #  @param num  The number of tuples to return.
    #  @param intimeof  A number that, when multiplied by the fraction
    #  itself, represents the sum of all the tuplets returned.
    #  @returns A list of num ratios that sum to the value of the Ratio.
    #
    #  Examples: Ratio(1,4).tuplets(3) returns three tuplets [1/12, 1/12, 1/12]
    #  which sum to Ratio(1,4).  Ratio(1,4).tuplets(3,2) returns three
    #  tuplets [1/6, 1/6, 1/6] which sum to ratio*2, or 1/2.
    def tuplets(self, num, intimeof=1):
        pass

    ## Returns the ratio representing num divisions of this ratio.
    #  @param num  The number to divide this ratio by.
    #  @return The new tuple value ratio.
    #
    #  Example:  Ratio(1,4).tup(5) is 1/20
    def tup(self, num):
        pass

    ## Returns the ratio as a floating point number.
    def float(self):
        pass

    ## Converts the ratio to floating point seconds according to a
    #  given tempo and beat:
    #  @param tempo  The tempo in beats per minute. Defaults to 60.
    #  @param beat  A ratio representing the beat. Defaults to 1/4 (quarter note).
    def seconds(self, tempo=60, beat=None):
        pass



if __name__ == '__main__':
    yeet = Ratio("1/4")

