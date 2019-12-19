from finalproj.score import Note, Pitch, Rest, Interval, Ratio, Mode, import_score
from finalproj.theory import Analysis, Rule, timepoints
from finalproj.species import *
from copy import copy
from math import inf
from glob import glob


samples = ['2-034-A_zawang2.musicxml',
           '2-028-C_hanzhiy2.musicxml',
           '2-000-B_sz18.musicxml',
           '2-003-A_cjrosas2.musicxml',
           '2-021-B_erf3.musicxml',
           '1-018-C_ajyanez2.musicxml',
           '2-003_A_chchang6.musicxml',
           '1-019-A_ajyanez2.musicxml',
           '2-009-C_mamn2.musicxml',
           '1-005-A_hanzhiy2.musicxml', #No direct unisons at #8 i'm pretty sure I'm correct tho - made a piazza post about it
           '2-010-B_mamn2.musicxml',
           '1-008-C_davidx2.musicxml', # at #1, marks consecutive fifths where not - asked on piazza
           '1-030_C_chchang6.musicxml',
           '2-034-C_zawang2.musicxml',
           '1-011-B_weikeng2.musicxml',
           '2-029-A_hanzhiy2.musicxml',
           '1-037-A_sz18.musicxml',
           '1-012-B_erf3.musicxml',
           '1-030-C_cjrosas2.musicxml',
           '2-009-B_mamn2.musicxml',
           '2-021-C_erf3.musicxml' # should not have 'At #7: consecutive fifths in cantus firmus notes',  should have 'At #4: consecutive fifths in cantus firmus notes',

           ]

#Start fixing this one
scorePaths = glob("C:/Users/qwert/School/MUS105/kjzhou2/finalproj/Species/2-034-C_zawang2.musicxml")
scriptpath = "C:/Users/qwert/School/MUS105/kjzhou2/finalproj/Species/"
# for i in range(len(samples)):
#     print('===================================================================')
#     print(samples[i])
#     s = import_score(scriptpath + samples[i])
#     if samples[i][0] == '1':
#         a = SpeciesAnalysis(s, 1)
#     else:
#         a = SpeciesAnalysis(s, 2)
#     print(a.submit_to_grading())
def int_from_err(s):
    i, j = s.index('#') + 1, s.index(':')

    return int(s[i:j])

s = import_score(scorePaths[0])
a = SpeciesAnalysis(s, 2)

results = a.submit_to_grading()

for s in sorted(results, key=int_from_err):
    print(s)

