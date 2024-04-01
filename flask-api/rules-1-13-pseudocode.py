from music21 import *

#filename = "../music-xml-examples/voice-leading-1.musicxml"
filename = "../music-generation/voice-leading-1-rns.mxl"
s = converter.parse(filename)

"""
print(len(s))

for n in s:
    print(n)

print()

for el in s.recurse():
    print(el)

s.write("MusicXML", "testing.musicxml")
"""

"""
s is a score object
s[2] = stream.PartStaff P1-Staff1
s[3] = stream.PartStaff P2-Staff2
s[2][1] = stream.Measure 1
s[2][1][4] = stream.Voice 1
s[2][1][4] = note.Note[4]

(music21.key.KeySignature) key = score[1][2]

Class ChordData
+ chord : music21.chord.Chord
+ 7th-chord : boolean
+ quality : string
+ inversion : integer
+ incomplete : boolean
+ harmonic_intervals : music21.interval.Interval[6] (stores B-T B-A B-S T-A T-S A-S)
+ melodic_intervals : music21.interval.Interval[6] (stores B-B', T-T', A-A', S-S')
+ numeral : music21.roman.RomanNumeral

Initialize chorddatas list with one ChordData object per beat

Class Error
+ i-start : integer
+ i-end : integer
+ type : string
+ voice : integer (0-3 for voice, 4 for whole chord)

Initialize list of errors

Parse chorddatas and check rules

1
If chord[0] > G5 or < C4
or chord[1] > C5 or < G3
or chord[2] > G4 or < C3
or chord[3] > C4 or < E2
Mark range error (voice #)

2
ChordData.harmonic_intervals[] (0:B-T 1:B-A 2:B-S 3:T-A 4:T-S 5:A-S)
If A-S >= P8 or T-A >= P8
Mark spacing error (whole chord)

3
Parse ChordData.harmonic_intervals
Call if interval.chromatic.direction < 0
Mark voice crossing error (whole chord)

4
S', A', T', B' are note values of next chord
For each interval in B-T', T-A', A-S'
If interval.chromatic.direction < 0
Mark voice overlapping error (whole chord)

5
Parse ChordData.melodic_intervals[] (B-B', T-T', A-A', S-S')
For each interval in melodic_intervals
If interval > P8
Mark large leap error (voice #)

6
For each interval i in melodic_intervals
    If i.name[1] to int > 2
        Retrieve i', melodic interval of same voice of next chord
        If i'.name[1] to int > 2    # two leaps in a row
            Define Chord c made up of current note and next two notes of same voice (3)
            If !(c.isMajorTriad OR c.isMinorTriad AND !(c.isIncompleteMajorTriad OR c.isIncompleteMinorTriad))    # must be a triad moving in consistent direction
                Mark multiple leap error (voice #)

7
For each interval i in melodic_intervals
    If i.name[1] to int > 4
        Retrieve i', melodic interval of same voice of next chord
            If (i'.name[1] to int != 2 OR i.chromatic.direction*-1 != i'.chromatic.direction)    # must move stepwise in opposite direction
                Mark melodic leap resolution error (voice #)

8    # could easily combine with rule 7
For each interval i in melodic_intervals
    If i.name[0] == "d"
        Retrieve i', melodic interval of same voice of next chord
            If (i'.name[1] to int != 2 OR i.chromatic.direction*-1 != i'.chromatic.direction)    # must move stepwise in opposite direction
                Mark melodic leap resolution error (voice #)
                
9
If music21.chord.Chord.seventh 
    7th = chord.closedPosition[-1].name
    Current chord = c, next chord = c'
    If c[0].name == 7th    # handle soprano exception first
        If !(c.romanNumeral == "V" AND c'.romanNumeral = "I" AND c'[0].name == key.pitchFromDegree(5).name)      # the one exception
            Mark improper resolution of 7th error (voice #)
        For n in 1-3
            If c[n].name == 7th
                i = interval(c[n], c'[n])
                If i.chromatic.direction != -1 OR i.name[1] != "2"
                    Mark improper resolution of 7th error (voice #)
                    
10     # consider improving this to catch chords that aren't in the key signature?
Chord c
If !(c.isMajorTriad OR c.isMinorTriad OR c.isAugmentedTriad OR c.isDiminishedTriad
OR c.isAugmentedSixth OR c.isSeventh)
    Mark non a chord harmony (whole chord)
    
11
For each interval i in harmonic_intervals
    If i == P8
        i' = same interval in following chord
        If i' == P8
            Mark parallel octaves (whole chord)

12    # doesn't check for secondary chords
For each interval i in harmonic_intervals
    If i == P5
        i' = same interval in following chord
        c = current chord
        If i' == P5
            If (c.isDiminishedSeventh OR c.isHalfDiminishedSeventh)
                7_hat = Note n where n.name == c.closedPosition[0]
                2_hat = Note n where n.name == c.closedPosition[1]
                4_hat = Note n where n.name == c.closedPosition[2]
                6_hat = Note n where n.name == c.closedPosition[3]
                If 6_hat > 4_hat AND c'[c.index(7_hat) == pitchFromDegree(8) AND
                                     c'[c.index(6_hat) == pitchFromDegree(5) AND
                                     c'[c.index(4_hat) == pitchFromDegree(3) AND
                                     c'[c.index(2_hat) == pitchFromDegree(3)
                    break;
            Mark parallel 5ths (whole chord)
                
13   # could use Alex's motion checker instead
If melodic_intervals[0].name[1] to int > 2 AND c'.harmonic_intervals[2] == (P5 or P8) AND melodic_intervals[0].chromatic.direction == melodic_intervals[3].chromatic.direction
    Mark hidden perfect intervals (whole chord)


dump() error list to json format and return
"""

#s.show()