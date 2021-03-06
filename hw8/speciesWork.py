from hw8.score import Note, Pitch, Rest, Ratio, Interval, Mode, import_score
from hw8.theory import Analysis, Rule, timepoints
from glob import glob
from copy import copy
###############################################################################

## You can import from score, theory, and any python system modules you want.

from math import inf

## Settings for a species 1 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a species 1 score. See also: SpeciesAnalysis.
s1_settings = {
    ## Maximum number of melodic unisons allowed.
    'MAX_UNI': 1,
    ## Maximum number of melodic 4ths allowed.
    'MAX_4TH': 2,
    ## Maximum number of melodic 5ths allowed.
    'MAX_5TH': 1,
    ## Maximum number of melodic 6ths allowed.
    'MAX_6TH': 0,
    ## Maximum number of melodic 7ths allowed.
    'MAX_7TH': 0,
    ## Maximum number of melodic 8vas allowed.
    'MAX_8VA': 0,
    ## Maximum number of leaps larger than a 3rd.
    'MAX_LRG': 2,
    ## Maximum number of consecutive melodic intervals moving in same direction.
    'MAX_SAMEDIR': 3,
    ## Maximum number of parallel consecutive harmonic 3rds/6ths.
    'MAX_PARALLEL': 3,
    ## Maximum number of consecutive leaps of any type.
    'MAX_CONSEC_LEAP': 2,
    ## Smallest leap demanding recovery step in opposite direction.
    'STEP_THRESHOLD': 5,
    # List of allowed starting scale degrees of a CP that is above the CF.
    'START_ABOVE': [1, 5],
    # List of allowed starting scale degrees of a CP that is below the CF.
    'START_BELOW': [1],
    # List of allowed melodic cadence patterns for the CP.
    'CADENCE_PATTERNS': [[2, 1], [7, 1]]
}

## Settings for species 2 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a second species score. See also: SpeciesAnalysis.
s2_settings = copy(s1_settings)
s2_settings['START_ABOVE'] = [1, 3, 5]
s2_settings['MAX_4TH'] = inf  # no limit on melodic fourths
s2_settings['MAX_5TH'] = inf  # no limit on melodic fifths
s2_settings['MAX_UNI'] = 0  # no melodic unisons allowed

## A list of all the possible result strings your analysis can generate.
# The {} marker in each string will always receive the 1-based integer index
# of the left-side time point that contains the offending issue. For example,
# if the first timepoint (e.g. self.timepoints[0]) contained an illegal
# starting pitch the message would be: 'At 1: forbidden starting pitch'
# Note: the variable result_strings does not need to be used by your code,
# it simply contains the list of all the result strings ;)
result_strings = [
    # VERTICAL RESULTS
    'At #{}: direct unisons', #1
    'At #{}: direct fifths', #2
    'At #{}: direct octaves', #3
    'At #{}: indirect unisons', #3 indirect means top voice cannot leap to these
    'At #{}: indirect fifths', #4
    'At #{}: indirect octaves', #5
    'At #{}: direct unisons in cantus firmus notes',  #6 if species 2 downbeat notes are also direct
    'At #{}: direct fifths in cantus firmus notes',  #7 if species 2
    'At #{}: direct octaves in cantus firmus notes',  #8 if species 2
    'At #{}: voice overlap', #9 top is lower than prev bottom or vice versa
    'At #{}: voice crossing', #10 check vertical interval if negative
    'At #{}: forbidden weak beat dissonance',  #11 vertical dissonance
    'At #{}: forbidden strong beat dissonance',  #12 vertical dissonance
    'At #{}: too many consecutive parallel intervals',  #13 parallel vertical intervals

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch', #14
    'At #{}: forbidden rest', #15
    'At #{}: forbidden duration', #16
    'At #{}: missing melodic cadence', #17
    'At #{}: forbidden non-diatonic pitch', #18
    'At #{}: dissonant melodic interval', #19
    'At #{}: too many melodic unisons',  #20 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',  #21 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',  #22 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',  #23 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',  #24 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',  #25 'MAX_8VA' setting
    'At #{}: too many large leaps',  #26 'MAX_LRG' setting
    'At #{}: too many consecutive leaps'  #27 'MAX_CONSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction',  #28 'MAX_SAMEDIR' setting
    'At #{}: too many consecutive parallel intervals',  #29 'MAX_PARALLEL' setting
    'At #{}: missing reverse by step recovery',  #30 'STEP_THRESHOLD' setting
    'At #{}: forbidden compound melodic interval', #31
]


## A class that implements a species counterpoint analysis of a given score.
# A SpeciesAnalysis has at least 5 attributes, you will very likely add more:
#
# * self.score  The score being analyzed.
# * self.species  The integer species number of the analysis, either 1 or 2.
# * self.settings  A settings dict for the analysis, either s1_settings or s2_settings.
# * self.rules  An ordered list of Rules that constitute your analysis.
# * self.results  A list of strings (see below) that constitute your analysis findings.
#
# You should call your analysis like this:
#
#   score = import_score(species1_xmlfile)
#   analysis = SpeciesAnalysis(score, 1, s1_settings)
#   analysis.submit_to_grading()
class SpeciesAnalysis(Analysis):
    ## Initializes a species analysis.
    # @param score A score containing a two-part species composition.
    # @param species A counterpoint species number, either 1 or 2.
    # @param settings A settings dict, either s1_settings or s2_settings.
    def __init__(self, score, species, settings):
        ## Call the superclass and give it the score.
        super().__init__(score)
        if species not in [1, 2]:
            raise ValueError(f"'{species}' is not a valid species number 1 or 2.")
        ## The integer species number for the analysis.
        self.species = species
        ## A local copy of the analysis settings.
        self.settings = copy(settings)
        ## Add your rules to this list.
        self.rules = [CPStartNote(self), CPMelodicCadence(self)]
        ## A list of strings that represent the findings of your analysis.
        self.results = []

        self.cpMelody = []
        self.cfMelody = []

    ## Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        tps = timepoints(self.score, span=True, measures=False)
        topMelody = []
        bottomMelody = []
        for t in tps:
            topMelody.append(t.nmap['P1.1'])
        for t in tps:
            bottomMelody.append(t.nmap['P2.1'])

        if self.score.get_part('P1').name == 'CP':
            self.cpMelody = topMelody
            self.cfMelody = bottomMelody
            self.cpIsTop = True
        elif self.score.get_part('P2').name == 'CP':
            self.cpMelody = bottomMelody
            self.cfMelody = topMelody
            self.cpIsTop = False
        cpZipMelody = list(zip(self.cpMelody[:-1], self.cpMelody[1:]))
        self.cpIntervals = [Interval(cpZipMelody[i][0].pitch, cpZipMelody[i][1].pitch) for i in range(len(cpZipMelody))]
        self.verticalIntervals = [Interval(bottomMelody[i].pitch, topMelody[i].pitch) for i in
                          range(len(topMelody))]


    ## This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        self.analyze()
        return self.results

###############################################################################

# A short list of files that contain lots of issues (see comments below)

samples = ['2-034-A_zawang2.musicxml', '2-028-C_hanzhiy2.musicxml', '2-000-B_sz18.musicxml',
           '2-003-A_cjrosas2.musicxml', '2-021-B_erf3.musicxml', '1-018-C_ajyanez2.musicxml',
           '2-003_A_chchang6.musicxml', '1-019-A_ajyanez2.musicxml', '2-009-C_mamn2.musicxml',
           '1-005-A_hanzhiy2.musicxml', '2-010-B_mamn2.musicxml', '1-008-C_davidx2.musicxml',
           '1-030_C_chchang6.musicxml', '2-034-C_zawang2.musicxml', '1-011-B_weikeng2.musicxml',
           '2-029-A_hanzhiy2.musicxml', '1-037-A_sz18.musicxml', '1-012-B_erf3.musicxml',
           '1-030-C_cjrosas2.musicxml', '2-009-B_mamn2.musicxml', '2-021-C_erf3.musicxml']

## Direct (parallel) 5ths, 8vas and unisons:
#     '1-037-A_sz18.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '2-000-B_sz18.musicxml'
## Direct motion measure to measure (species 2):
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
## Indirect (hidden) 5ths and 8vas:
#     '1-030_C_chchang6.musicxml'
#     '1-008-C_davidx2.musicxml'
#     '1-030-C_cjrosas2.musicxml'
#     '1-011-B_weikeng2.musicxml'
## Voice overlap:
#     '1-005-A_hanzhiy2.musicxml'
#     '1-019-A_ajyanez2.musicxml'
## Maximum parallel interval:
#     '1-037-A_sz18.musicxml'
## Voice crossing:
#     '1-019-A_ajyanez2.musicxml'
## Disjunction:
#     '1-008-C_davidx2.musicxml'
## Weak beat dissonance not passing tone (species 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
#     '2-021-C_erf3.musicxml'
## Strong beat dissonance (species 1 and 2):
#     '2-000-B_sz18.musicxml'
#     '2-034-C_zawang2.musicxml'
## Wrong durations:
#     '2-009-C_mamn2.musicxml'
#     '2-034-A_zawang2.musicxml'
#     '2-021-B_erf3.musicxml'
#     '2-009-B_mamn2.musicxml'
#     '2-021-C_erf3.musicxml'
## Not diatonic:
#     '1-018-C_ajyanez2.musicxml'
#     '2-003-A_cjrosas2.musicxml'
#     '2-003_A_chchang6.musicxml'
## Starting pitch:
#     '2-028-C_hanzhiy2.musicxml'
#     '1-012-B_erf3.musicxml'
## Melodic cadence:
#     '1-018-C_ajyanez2.musicxml'
#     '1-030_C_chchang6.musicxml'
#     '2-034-A_zawang2.musicxml'
## Too many 'x':
#     '2-029-A_hanzhiy2.musicxml'
#     '2-003_A_chchang6.musicxml'
#     '2-010-B_mamn2.musicxml'
## Reverse after leap:
#     '2-029-A_hanzhiy2.musicxml'
#     '2-010-B_mamn2.musicxml'

class CPStartNote(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if the starting note is correct or just a rest")
        self.analysis = analysis
        self.score = analysis.score
        self.scale = self.score.metadata['main_key'].scale()
        self.setting = analysis.settings

    def apply(self):
        cpMelody = self.analysis.cpMelody
        cpIsTop = self.analysis.cpIsTop
        self.results = self.analysis.results
        if cpIsTop:
            startingPC = self.setting['START_ABOVE']
        else:
            startingPC = self.setting['START_BELOW']
        startingPitch = cpMelody[0].pitch.pnum()
        startingNotes = [self.scale[i - 1] for i in startingPC]
        if startingPitch not in startingNotes:
            self.results.append(addToResults(0, result_strings[14]))

class CPMelodicCadence(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks for the melodic cadence in both voices")
        self.analysis = analysis
        self.score = analysis.score
        self.scale = self.score.metadata['main_key'].scale()
        self.setting = analysis.settings

    def apply(self):
        self.results = self.analysis.results
        cadPatterns = self.setting['CADENCE_PATTERNS'] #[[2,1],[7,1]]
        cadencePatterns = []
        for i in range(len(cadPatterns)):
            pitchPattern = []
            for j in range(len(cadPatterns[i])):
                print(cadPatterns[i][j])
                pitchPattern.append(self.scale[cadPatterns[i][j] - 1])
            cadencePatterns.append(pitchPattern)
        print(cadencePatterns)
        cpLast2 = [self.analysis.cpMelody[i].pitch.pnum() for i in range(-2, 0)]
        cfLast2 = [self.analysis.cfMelody[i].pitch.pnum() for i in range(-2, 0)]
        print(cpLast2)
        print(cfLast2)
        if cpLast2 in cadencePatterns:
            del cadencePatterns[cadencePatterns.index(cpLast2)]
            if cfLast2 not in cadencePatterns:
                self.results.append(addToResults(len(self.analysis.cpMelody) - 2, result_strings[17]))
        else:
            self.results.append(addToResults(len(self.analysis.cpMelody) - 2, result_strings[17]))

def addToResults(tp, resultString):
    return resultString.format(tp + 1)



scorePaths = glob("C:/Users/qwert/School/MUS105/Species/1-001*.musicxml")
s = import_score(scorePaths[0])
print(s)
a = SpeciesAnalysis(s, 1, s1_settings)
print(a.submit_to_grading())


