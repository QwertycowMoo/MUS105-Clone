###############################################################################

from enum import Enum

## A barline represents the right or left side delimiter of a bar.  The set
# of bar lines are: STANDARD, DOTTED, DASHED, TICKED, SHORT, HEAVY,
# INTERIOR_DOUBLE, FINAL_DOUBLE, LEFT_REPEAT, RIGHT_REPEAT, MIDDLE_REPEAT.
# The enum values do not matter, you can use enum.auto() to assign them.
# See: https://en.wikipedia.org/wiki/Bar_(music)
class Barline (Enum):
    # Create enums here...
    STANDARD = 0
    DOTTED = 1
    DASHED = 2
    TICKED = 3
    SHORT = 4
    HEAVY = 5
    INTERIOR_DOUBLE = 6
    FINAL_DOUBLE = 7
    LEFT_REPEAT = 8
    RIGHT_REPEAT = 9
    MIDDLE_REPEAT = 10


