###############################################################################

## You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy


## A template dictionary whose keys represent analytical checks performed on
# a melody. Your analysis will copy this dictionary into its self.results
# attribute and then run its rules to update the value of each check in the
# dictionary. When a rule is run and it determines a check is successful, the
# rule will set the dictionary value (e.g. self.analysis['MEl_START_NOTE'])
# to True and if its not successful it will set it to a list of zero or more
# values as described below.
melodic_checks = {
    
    # Pitch checks

    ## Starting note must be tonic, mediant, or dominant. If the melody
    # starts correctly set this value to True, otherwise set it to an empty
    # list [].
    'MEL_START_NOTE': None,

    ## Last two notes must be melodic cadence (2-1 or 7-1). If the
    # melody ends correctly set this value to True, otherwise set
    # it to an empty list [].
    'MEL_CADENCE': None,

    ## At least 75% of notes must be within the tessitura (central Major
    # 6th of the melody's range). If the check is successful set this value
    # to true, otherwise set it to an empty list [].
    'MEL_TESSITURA': None,

    ## All pitches must be diatonic. If the check is successful set
    # this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start
    # on 1 not 0.
    'MEL_DIATONIC': None,

    # Melodic interval checks

    ## At least 51% of notes must be stepwise.  If the check is successful
    # set this value to True, otherwise set it to an empty list [].
    'INT_STEPWISE': None,

    ## All intervals must be consonant (P4 is consonant). If the check
    # is successful set this value to True, otherwise set it to a list
    # containing the note positions of each note that fails. Note
    # positions start on 1 not 0. Since this check involves an interval
    # between two notes, use the position of the note to the left
    # of the offending interval.
    'INT_CONSONANT': None,

    ## All intervals must be an octave or less. If the check is successful
    # set this value to True, otherwise set it to a list containing the
    # note positions of each note that fails. Note positions start on 1
    # not 0. Since this check involves an interval between two notes, use
    # the position of the note to the left of the offending interval.
    'INT_SIMPLE': None,

    ## Max number of large leaps is 1. A large leap is defined as a perfect
    # fifth or more. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each
    # interval after the first one.
    'INT_NUM_LARGE': None,

    ## Max number of unisons is 1. If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each unison after the first one.
    'INT_NUM_UNISON': None,

    ## Max number of consecutive intervals moving in same direction is 3
    # (i.e four consecutive notes). If the check is successful set this
    # value to True, otherwise set it to a list containing the note
    # positions of each interval after the third one.
    'INT_NUM_SAMEDIR': None,

    # Leap checks

    ## Leap of 4th must reverse direction, leap of 5th or more must reverse
    # by step. The leap can be the result of a single interval or by multiple
    # consecutive leaps in the same direction. For multiple leaps in the same
    # direction, the total size of the leap should be the sum of all the leaps
    # in the same direction. If the check is successful set this value to True,
    # otherwise set it to a list containing the note positions of each interval
    # that fails. To mark a leap spanning a 5th or greater that did not reverse
    # by step, set its note index to be negative.
    # Anything larger than a second is a leap
    # Consecutive thirds are ok tho, 2 in a row outlines a triad. More than 2 is nono
    # Three leaps in a row
    # Leap a fourth, can leap a third after that
    # Leap anything larger, must be stepwise in opposite
    # Only check for the first after the leap
    'LEAP_RECOVERY': None,

    ## Max number of consecutive leaps in a row is 2 (three notes). If the
    # check is successful set this value to True, otherwise set it to a list
    # containing the note positions of each interval after the second leap.
    'LEAP_NUM_CONSEC': None,

    # Shape checks

    ## Max number of climax notes is 1.  If the check is successful set
    # this value to True, otherwise set it to a list containing the note
    # positions of each climax after the first.
    'SHAPE_NUM_CLIMAX': None,

    ## Climax note must be located within the center third of melody.  If
    # the check is successful set this value to True, otherwise set it to a
    # list containing the note positions of all climaxes outside it.
    'SHAPE_ARCHLIKE': None,

    ## A set of intervals with at least one direct repetition cannot
    # occupy more than 50% of melody. If the check is successful set this
    # value to True, otherwise set it to a list containing the set of
    # interval motions (e.g [2, 2, -3].
    'SHAPE_UNIQUE': None
}


def getNotes(score, p, s, v):
    data = []
    for b in score.parts[p].staffs[s]:
        data += b.voices[v]
    return data

# Here is an example of a rule. You can define as many rules as you want.
# The purpose of running a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class MyFirstRule(Rule):

    ## Rule initializer.
    def __init__(self, analysis):
        ## Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "My very first rule.")
        # Now initialize whatever attributes your rule defines.
        # ...

    ## This is where your rule does all its work. When the work is done you
    # should update the analysis results with whatever checks it is doing.
    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

#    ## Uncomment this code if you want your rule to print information to the
#    # the terminal just after it runs...
#    def display(self, index):
#        print('-------------------------------------------------------------------')
#        print(f"Rule {index+1}: {self.title}")
#        print("I'm here!")


# ...ADD MORE RULES HERE!....
class MelStartNote(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "The starting note is tonic, mediant, and dominant")
        self.score = analysis.score
        self.results = analysis.results
        self.scale = self.score.metadata['main_key'].scale()
        self.firstPitch = self.score.parts[0].staffs[0].bars[0].voices[0].notes[0].pitch.pnum()

    def apply(self):
        if self.firstPitch == self.scale[0]:
            self.results['MEL_START_NOTE'] = True
        elif self.firstPitch == self.scale[2]:
            self.results['MEL_START_NOTE'] = True
        elif self.firstPitch == self.scale[4]:
            self.results['MEL_START_NOTE'] = True
        else:
            self.results['MEL_START_NOTE'] = []

class MelCadence(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The last two notes are in a 2-1/7-1 cadence')
        self.score = analysis.score
        self.results = analysis.results
        self.scale = self.score.metadata['main_key'].scale()
        self.notes = getNotes(self.score, 0, 0, 0)
    def apply(self):
        secondLast = self.notes[-2].pitch.pnum()
        last = self.notes[-1].pitch.pnum()
        if last == self.scale[0]:
            if secondLast == self.scale[6]:
                self.results['MEL_CADENCE'] = True
            elif secondLast == self.scale[1]:
                self.results['MEL_CADENCE'] = True
            else:
                self.results['MEL_CADENCE'] = []
        else:
            self.results['MEL_CADENCE'] = []

class MelTessitura(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The majority(75%) is within the tessitura')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        top = max(self.notes).pitch
        bottom = min(self.notes).pitch
        middle = int((top.keynum() + bottom.keynum()) / 2)
        bPitch = Pitch.from_keynum(middle - 4)
        tPitch = Pitch.from_keynum(middle + 5)
        inTess = 0
        for note in self.notes:
            if note.pitch >= bPitch and note.pitch <= tPitch:
                inTess += 1
        if (inTess / len(self.notes) >= .75):
            self.results['MEL_TESSITURA'] = True
        else:
            self.results['MEL_TESSITURA'] = []

class MelDiatonic(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The piece is diatonic')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)
        self.key = analysis.score.metadata['main_key']

    def apply(self):
        print(self.key.scale())
        scale = self.key.scale()
        extraHarmonic = (Interval('+1').transpose(self.key.scale()[6]))
        extraMelodic = (Interval('+1').transpose(self.key.scale()[5]))
        scale.append(extraHarmonic)

        wrongNotes = []
        for i in range(len(self.notes)):
            if self.notes[i].pitch.pnum() not in scale:
                wrongNotes.append(i + 1)
        if len(wrongNotes) == 0:
            self.results['MEL_DIATONIC'] = True
        else:
            self.results['MEL_DIATONIC'] = wrongNotes

class IntStepwise(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The piece is mostly stepwise')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        rip = zip(self.notes[:-1], self.notes[1:])
        stepwiseCount = 0
        for i in rip:
            interval = Interval(i[0].pitch, i[1].pitch)
            if interval.is_second():
                stepwiseCount += 1
        if (stepwiseCount / len(self.notes)) >= .5:
            self.results['INT_STEPWISE'] = True
        else:
            self.results['INT_STEPWISE'] = []

class IntConsonant(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The intervals are all consonant')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        rip = list(zip(self.notes[:-1], self.notes[1:]))
        wrongIntervals = []
        for i in range(len(rip)):
            interval = Interval(rip[i][0].pitch, rip[i][1].pitch)
            if interval.is_second() or interval.is_unison():
                pass
            else:
                if interval.is_dissonant():
                    wrongIntervals.append(i + 1)
        if len(wrongIntervals) == 0:
            self.results['INT_CONSONANT'] = True
        else:
            self.results['INT_CONSONANT'] = wrongIntervals

class IntSimple(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'The intervals are all simple')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        rip = list(zip(self.notes[:-1], self.notes[1:]))
        wrongIntervals = []
        for i in range(len(rip)):
            interval = Interval(rip[i][0].pitch, rip[i][1].pitch)
            if interval.is_compound():
                wrongIntervals.append(i + 1)
        if len(wrongIntervals) == 0:
            self.results['INT_SIMPLE'] = True
        else:
            self.results['INT_SIMPLE'] = wrongIntervals

class IntNumLarge(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'There are no more than 1 large leap over a perfect fifth')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        rip = list(zip(self.notes[:-1], self.notes[1:]))
        wrongIntervals = []
        numWrong = 0
        for i in range(len(rip)):
            interval = Interval(rip[i][0].pitch, rip[i][1].pitch)
            if interval >= Interval('P5'):
                numWrong += 1
                if numWrong > 1:
                    wrongIntervals.append(i + 1)
        if len(wrongIntervals) > 0:
            self.results['INT_NUM_LARGE'] = wrongIntervals
        else:
            self.results['INT_NUM_LARGE'] = True

class IntNumUnison(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'There are no more than 1 occurances of a union')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)
    def apply(self):
        rip = list(zip(self.notes[:-1], self.notes[1:]))
        wrongIntervals = []
        numWrong = 0
        for i in range(len(rip)):
            interval = Interval(rip[i][0].pitch, rip[i][1].pitch)
            if interval.is_unison():
                numWrong += 1
                if numWrong > 1:
                    wrongIntervals.append(i + 1)
        if len(wrongIntervals) > 0:
            self.results['INT_NUM_UNISON'] = wrongIntervals
        else:
            self.results['INT_NUM_UNISON'] = True

class IntNumSameDir(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'There are no more than 1 large leap over a perfect fifth')
        self.score = analysis.score
        self.results = analysis.results
        self.notes = getNotes(self.score, 0, 0, 0)

    def apply(self):
        rip = list(zip(self.notes[:-1], self.notes[1:]))
        wrongNotes = []
        isAscending = True
        inARow = 0
        for i in range(len(rip)):
            interval = Interval(rip[i][0].pitch, rip[i][1].pitch)
            if interval.is_ascending() != isAscending:
                isAscending = not isAscending
                inARow = 0
            inARow += 1
            if inARow > 3:
                wrongNotes.append(i + 2)
        if len(wrongNotes) > 0:
            self.results['INT_NUM_SAMEDIR'] = wrongNotes
        else:
            self.results['INT_NUM_SAMEDIR'] = True

class LeapRecovery(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, 'Checks for law of recovery')
        self.score = analysis.score
        self.results = analysis.results
        self.analysis = analysis

    def apply(self):
        self.notes = self.analysis.melody
        self.intervals = self.analysis.intervals
        print(self.intervals)
        spans = [(i.span + 1) * i.sign for i in self.intervals]
        print(spans)
        wrongNotes = []
        prev = 0
        for i in range(1, len(spans) + 1):
            prev = prev + spans[i - 1] if prev >= 3 and abs(prev + spans[i - 1]) > prev else spans[i - 1]
            print(prev)
            try:
                now = spans[i]
            except IndexError:
                now = prev
            if abs(prev) > 3:
                if abs(prev) > 4:
                    if prev < 0:
                        if not(now > 0 and now <= 2):
                            wrongNotes.append((i + 1) * -1)
                    elif prev > 0:
                        if not(now < 0 and now >= -2):
                            wrongNotes.append((i + 1) * -1)
                    else:
                        wrongNotes.append((i + 1) * -1)
                else:
                    if (prev > 0 and now > 0) or (prev < 0 and now < 0):
                        wrongNotes.append((i + 1))

        if len(wrongNotes) == 0:
            self.results['LEAP_RECOVERY'] = True
        else:
            self.results['LEAP_RECOVERY'] = wrongNotes

## A class representing a melodic analysis of a voice in a score. The class
# has three attributes to being with, you will likely add more attributes.
# * self.score: The score passed into the analysis
# * self.rules: A list of rules that you define to implement the analysis
# * self.results: A dictionary containing the set of analytical checks your
# analysis performs. Your rules will update specific checks in this dictionary.
class MelodicAnalysis(Analysis):
    def __init__(self, score):
        ## Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        ## Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)
        ## Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [MyFirstRule(self), MelStartNote(self), MelCadence(self), MelTessitura(self), MelDiatonic(self)
                      , IntStepwise(self), IntConsonant(self), IntSimple(self), IntNumLarge(self), IntNumUnison(self)
                      , IntNumSameDir(self), LeapRecovery(self)]

    def cleanup(self):
        self.melody, self.intervals, self.motions = [], [], []

    ## You MUST define a setup function! A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Call: analyze('pvid')"
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        melodic_id = args[0]
        tps = timepoints(self.score, span=True, measures=False)
        self.melody = []
        for t in tps:
            self.melody.append(t.nmap[melodic_id])
        pitches = list(zip(self.melody[:-1], self.melody[1:]))
        self.intervals = [Interval(pitches[i][0].pitch, pitches[i][1].pitch) for i in range(len(pitches))]

    ## This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

#from hw8.laitz82 import *
#s = import_score("C:/Users/qwert/School/MUS105/kjzhou2/hw8/xmls/Laitz_p84A.musicxml")
#a = MelodicAnalysis(s)