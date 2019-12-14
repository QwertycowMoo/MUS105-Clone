from finalproj.score import Note, Pitch, Rest, Interval, Ratio, Mode, import_score
from finalproj.theory import Analysis, Rule, timepoints
from finalproj.species import *
from copy import copy
from math import inf
from glob import glob

scorePaths = glob("C:/Users/qwert/School/MUS105/kjzhou2/finalproj/Species/2-034-A_zawang2.musicxml")
s = import_score(scorePaths[0])
print(s)
a = SpeciesAnalysis(s, 2)
print(a.submit_to_grading())
