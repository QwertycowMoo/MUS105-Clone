from hw8.score import Pitch, Interval, Mode, import_score
from hw8.theory import Analysis, Rule, timepoints
from enum import Enum, auto

s = import_score("C:/Users/qwert/School/MUS105/Laitz Melodic Scores/Laitz_p84A.musicxml")
print(s)
print(s.metadata)
tps = timepoints(s, measures = False)
print(tps)
for t in tps: print(t.nmap)
mel = [t.nmap['P1.1'] for t in tps]
print(mel)