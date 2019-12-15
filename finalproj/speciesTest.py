from finalproj.score import Note, Pitch, Rest, Interval, Ratio, Mode, import_score
from finalproj.theory import Analysis, Rule, timepoints
from finalproj.species import *
from copy import copy
from math import inf
from glob import glob


samples = ['2-034-A_zawang2.musicxml', # consecutive intervals at #7, direct fifths needs to be 1 -,#20 consecutive octaves should not be there
           '2-028-C_hanzhiy2.musicxml',
           '2-000-B_sz18.musicxml', #recognizes #18 error as missing melodic cadence instead of consecutive octaves so hmm
           '2-003-A_cjrosas2.musicxml',
           '2-021-B_erf3.musicxml',
           '1-018-C_ajyanez2.musicxml',
           '2-003_A_chchang6.musicxml',
           '1-019-A_ajyanez2.musicxml',
           '2-009-C_mamn2.musicxml',
           '1-005-A_hanzhiy2.musicxml',
           '2-010-B_mamn2.musicxml',
           '1-008-C_davidx2.musicxml',
           '1-030_C_chchang6.musicxml',
           '2-034-C_zawang2.musicxml',
           '1-011-B_weikeng2.musicxml',
           '2-029-A_hanzhiy2.musicxml',
           '1-037-A_sz18.musicxml',
           '1-012-B_erf3.musicxml',
           '1-030-C_cjrosas2.musicxml',
           '2-009-B_mamn2.musicxml',
           '2-021-C_erf3.musicxml'
           ]

#Start fixing this one
scorePaths = glob("C:/Users/qwert/School/MUS105/kjzhou2/finalproj/Species/2-003-A_cjrosas2.musicxml")
s = import_score(scorePaths[0])
print(s)
a = SpeciesAnalysis(s, 2)
for output in a.submit_to_grading():
    print(output)
