###############################################################################

from enum import Enum, auto

## A barline represents the right or left side delimiter of a bar.  The set
# of bar lines are: STANDARD, DOTTED, DASHED, TICKED, SHORT, HEAVY,
# INTERIOR_DOUBLE, FINAL_DOUBLE, LEFT_REPEAT, RIGHT_REPEAT, MIDDLE_REPEAT.
# The enum values do not matter, you can use enum.auto() to assign them.
# See: https://en.wikipedia.org/wiki/Bar_(music)
class Barline (Enum):
    # Create enums here...
    STANDARD = Enum.auto()
    DOTTED = Enum.auto()
    DASHED = Enum.auto()
    TICKED = Enum.auto()
    SHORT = Enum.auto()
    HEAVY = Enum.auto()
    INTERIOR_DOUBLE = Enum.auto()
    FINAL_DOUBLE = Enum.auto()
    LEFT_REPEAT = Enum.auto()
    RIGHT_REPEAT = Enum.auto()
    MIDDLE_REPEAT = Enum.auto()


